import asyncio
import logging
import os
import signal
import socket
import random
import uuid

import prometheus_client
import opentelemetry.sdk.resources
import opentelemetry.sdk.trace
import opentelemetry.sdk.trace.export
import opentelemetry.trace
from opentelemetry.exporter.otlp.proto.grpc import trace_exporter
from pythonjsonlogger import jsonlogger


LATENCY = prometheus_client.Histogram('job_latency_seconds', 'Job latency',
                                      ['stage'])
FAILURES = prometheus_client.Counter('job_failures_total', 'Job failure count')
IN_FLIGHT = prometheus_client.Gauge('system_in_flight_total',
                                    'Concurrent jobs')

STATE = prometheus_client.Enum('job_state', 'Current job state',
                               states=['extract', 'transform', 'load'])
VERSION = prometheus_client.Info('worker_version', 'Current worker version')


logger = logging.getLogger('app.main')
tracer = opentelemetry.trace.get_tracer(__name__)


# These don't seem to work with async methods
# @IN_FLIGHT.track_inprogress()
# @FAILURES.count_exceptions()
async def worker(version: int) -> None:
    """
    metrics:
      count concurrent jobs (gauge)
      count errors (counter)
      measure job latency, per state (histogram)
      worker version & hostname (info)  # TODO: what's an info?
      job state (enum)  # TODO: what's an enum?

    logging:
      TODO

    tracing:
      TODO
    """
    with tracer.start_as_current_span('worker'):
        IN_FLIGHT.inc()
        try:
            VERSION.info({'version': f'x.y.{version}',
                          'host': socket.gethostname()})

            with tracer.start_as_current_span('extract'):
                with LATENCY.labels('extract').time():
                    STATE.state('extract')
                    job_id = str(uuid.uuid4())
                    job_kind = random.choice(['foo', 'bar', 'baz'])
                    trace = (opentelemetry.trace.get_current_span()
                             .get_span_context().trace_id)
                    logger.info('starting job',
                                extra={'id': job_id,
                                       'kind': job_kind,
                                       'trace': f'{trace:032x}'})
                    if random.random() < 0.01:
                        raise Exception('failed to extract')

            with tracer.start_as_current_span('transform'):
                with LATENCY.labels('transform').time():
                    STATE.state('transform')
                    failure_ratio = 0.1 if job_kind == 'foo' else 0.05
                    if random.random() < failure_ratio:
                        await asyncio.sleep(0.1)
                        raise Exception('failed to transform')
                    else:
                        await asyncio.sleep(random.paretovariate(1))

            with tracer.start_as_current_span('load'):
                with LATENCY.labels('load').time():
                    STATE.state('load')
                    if random.random() < 0.02:
                        raise Exception('failed to load')
        except Exception:
            FAILURES.inc()
            raise
        finally:
            IN_FLIGHT.dec()


class Shutdown:
    quit = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.trigger)
        signal.signal(signal.SIGTERM, self.trigger)

    def trigger(self):
        self.quit = True


async def main() -> None:
    # start prometheus server -- this is in a thread, will asyncio have issues?
    prometheus_client.start_http_server(8080)

    # graceful shutdown handler for k8s SIGTERMs etc
    shutdown = Shutdown()

    try:
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
        # generic asyncio graceful shutdown code
        tasks = [t for t in asyncio.all_tasks()
                 if t is not asyncio.current_task()]
        if not tasks:
            return

        logger.info(f'awaiting {len(tasks)} tasks')
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

    provider = opentelemetry.sdk.trace.TracerProvider(
        resource=opentelemetry.sdk.resources.Resource(attributes={
            opentelemetry.sdk.resources.SERVICE_NAME: 'app',
        }))
    # N.B. the namespace would be constant if not for the cluster->namespace
    # hack used to test multi-cluster
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
