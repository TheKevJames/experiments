import asyncio
import logging
import os
import signal
import socket
import random
import uuid

# We'll be using the prometheus_client for metrics, the builtin logging library
# for logging, and the opentelemetry client for tracing. The opentelemetry
# client promises to replace the former two as well to make it easier to manage
# all three componenets from one place, but it isn't there quite yet. Once it
# is, using otel libraries for all three may be better!
import prometheus_client
import opentelemetry.sdk.resources
import opentelemetry.sdk.trace
import opentelemetry.sdk.trace.export
import opentelemetry.trace
from opentelemetry.exporter.otlp.proto.grpc import trace_exporter


# Prometheus requires you to create metrics as follows. Any metrics defined in
# this way will be made available later on via the builtin metrics server.
#
# The latency, failures, and in_flight metrics define the three basic metric
# kinds: histograms, counters, and gauges. The Prometheus docs are your best
# bet for learning more:
# https://prometheus.io/docs/practices
LATENCY = prometheus_client.Histogram('job_latency_seconds', 'Job latency',
                                      ['stage'])
FAILURES = prometheus_client.Counter('job_failures_total', 'Job failure count')
IN_FLIGHT = prometheus_client.Gauge('system_in_flight_total',
                                    'Concurrent jobs')

# TODO: I haven't actually figured out the value of Enum and Info type metrics
# yet, they seem woefully undocumented. I suspect that once this demo supports
# examplars these might make more sense.
STATE = prometheus_client.Enum('job_state', 'Current job state',
                               states=['extract', 'transform', 'load'])
VERSION = prometheus_client.Info('worker_version', 'Current worker version')


# Like the metrics, we must initialize our logger and tracer. Note that I'm
# using `app.main` here rather than `__name__` by convention; since Python sets
# `__name__ == '__main__'` for your entrypoint, it can be a good idea to set
# this explicitly and rely on `__name__` everywhere else in your codebase to
# ensure everything is consistent.
# The exact value is irrelevant for purposes of this demo.
logger = logging.getLogger('app.main')
tracer = opentelemetry.trace.get_tracer('app.main')


# Theoretically, the Prometheus SDK is meant to support decorators for some
# common cases, which would have made this demo simpler. In practice, they do
# not currently support async methods. There are various libs such as
# prometheus-async to solve this, if you want the convenience of:
# @IN_FLIGHT.track_inprogress()
# @FAILURES.count_exceptions()
async def worker(version: int) -> None:
    # All work will be performed within a parent span named "worker".
    with tracer.start_as_current_span('worker'):
        # The IN_FLIGHT metric will track the current number of jobs being
        # actively worked on. We'll decrement this once we're done.
        IN_FLIGHT.inc()
        try:
            # TODO: see Enum/Info
            VERSION.info({'version': f'x.y.{version}',
                          'host': socket.gethostname()})

            # We'll create a sub-span for each stretch of our sample ETL
            # process. Since traces can be arbitrarily nested, we will be able
            # to reference the parent/child/sibling traces as need be.
            with tracer.start_as_current_span('extract'):
                # We'll be tracking the latency for each step of the process.
                # Note that some labels are constant (eg. such as the name of
                # this pod) and some can be added on-the-fly. For those added
                # at runtime, they must be predefined in the metric config --
                # in this case, `extract` matches the `['stage']` definition
                # above. By the end of this method, we'll have defined the
                # latency metric with three values for this tag (eg.
                # `latency{stage=extract}`, `latency{stage=transform}`, and
                # `latency{stage=load}`.
                with LATENCY.labels('extract').time():
                    # TODO: see Enum/Info
                    STATE.state('extract')

                    # Generate some random data here to give our metrics some
                    # flavour when we get to aggregation and exploration.
                    job_id = str(uuid.uuid4())
                    job_kind = random.choice(['foo', 'bar', 'baz'])
                    # The trace can be fetched directly which lets us, for
                    # example, log traces which would be interesting to
                    # investigate. In our demo, everything is interesting!
                    trace = (opentelemetry.trace.get_current_span()
                             .get_span_context().trace_id)
                    logger.info('starting job %s:%s with trace %032x',
                                job_kind, job_id, trace)

                    # Fail randomly 1% of the time. We should see the failure
                    # rate of tasks in the extract stage match this value later
                    # on.
                    if random.random() < 0.01:
                        raise Exception('failed to extract')

            with tracer.start_as_current_span('transform'):
                with LATENCY.labels('transform').time():
                    STATE.state('transform')
                    # Different failure rates for different job types
                    failure_ratio = 0.1 if job_kind == 'foo' else 0.05
                    if random.random() < failure_ratio:
                        await asyncio.sleep(0.1)
                        raise Exception('failed to transform')
                    else:
                        # Our latency will model a pareto distribution to make
                        # debugging fun. This puts the 90th percentile just
                        # below 10s.
                        await asyncio.sleep(random.paretovariate(1))

            with tracer.start_as_current_span('load'):
                with LATENCY.labels('load').time():
                    STATE.state('load')
                    if random.random() < 0.02:
                        raise Exception('failed to load')
        except Exception:
            # We'll count failures without attaching a label for the failure
            # cause: later, we'll be able to use metric->trace exemplars to
            # determine this value.
            FAILURES.inc()
            raise
        finally:
            IN_FLIGHT.dec()


# Nothing to see here, just a simple way to catch k8s exit signals and shutdown
# gracefully.
class Shutdown:
    quit = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.trigger)
        signal.signal(signal.SIGTERM, self.trigger)

    def trigger(self, _signo, _frame):
        self.quit = True


async def main() -> None:
    shutdown = Shutdown()

    try:
        # TODO: see Enum/Info
        version = 1
        while not shutdown.quit:
            asyncio.create_task(worker(version))
            await asyncio.sleep(random.random())
            if random.random() < 0.001:
                version += 1
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info('shutting down by request')
    except Exception:
        logger.exception('got unhandled exception')
    finally:
        # More irrelevant and generic asyncio graceful shutdown code.
        tasks = [t for t in asyncio.all_tasks()
                 if t is not asyncio.current_task()]
        if not tasks:
            return

        logger.info(f'awaiting {len(tasks)} tasks')
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    # This encapsulates the basic library vs application divide: your library
    # code will describe what logs/metrics/etc to emit and your application
    # will describe what to do with those things. In this case, we'll keep it
    # simple:

    # Initialize logging without any special configs. Loki will need to know
    # how to scrape your logs (ie. what format they emit) and supports
    # arbitrary formats... but it supports the default logging format with no
    # special config, so that'll make our lives easiest.
    # These will just get sent to stdout, which Promtail knows how to scrape
    # and can forward along to Loki.
    logging.basicConfig(level=logging.INFO)

    # Start the builtin Prometheus metrics server. This will expose our app's
    # metrics on port 8080, which we'll scrape later via Prometheus instances
    # in our cluster which will forward those metrics along to Thanos/long-term
    # storage.
    prometheus_client.start_http_server(8080)

    # Initialize the OpenTelemetry tracing SDK to push traces to the Grafana
    # Agent, which will in turn forward them to Tempo.
    # Note that while your metrics and logs are pulled from your application,
    # traces will be pushed. This seems to be a deliberate design decision in
    # all trace clients I've played with.
    provider = opentelemetry.sdk.trace.TracerProvider(
        resource=opentelemetry.sdk.resources.Resource(attributes={
            opentelemetry.sdk.resources.SERVICE_NAME: 'app',
        }))
    # N.B. the namespace would be constant here if not for the
    # cluster->namespace hack used to run the "multi-cluster" example on a
    # single cluster.
    namespace = os.environ['POD_NAMESPACE'].replace('default', 'monitoring')
    provider.add_span_processor(
        opentelemetry.sdk.trace.export.BatchSpanProcessor(
            trace_exporter.OTLPSpanExporter(
                endpoint=f'http://grafana-agent.{namespace}.svc:4317',
                insecure=True)))
    opentelemetry.trace.set_tracer_provider(provider)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
