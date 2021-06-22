Observability Demo
==================

This project defines a sample set of k8s clusters instrumented with metrics
(Prometheus), logging (Loki), and tracing (Tempo) -- ie. "The Observability
Stack". It can be deployed to any kubernetes cluster as a demo, but the overall
goal is to *read through it and understand how to fit it into your own systems*
-- I've attempted to keep things as straightforward as possible to allow you to
understand each piece rather than making use of Helm/Jsonnet/Tanka/etc: if
you're just looking for a simple method to deploy these components, the
official Helm charts/Operators/whatever-method-you-like would be a good place
to look.

This demo is divided into two cluster types: application and reporting
clusters. The idea here being that we should be able to scale each
independently, maintain high availability of your monitoring infrastructure,
and keep the impact on your application workloads as lightweight as possible.

Application clusters are those you want to monitor, eg. the existing systems
you already have if you're jsut getting started with monitoring. These will
include the bare minimum for ingestion of metrics, logging, and traces, with as
little actual processing as possible. These should be able to scale to
arbitrarily many clusters running arbitrarily many applications.

Reporting clusters are the aggregation layer which ingest all your monitoring
data and let you build dashboards/write queries/generate alerts/etc. These
should be able to scale independently of your application clusters and should
allow you to run as many as you'd like in parallel, according to your risk
appetite.

Your first step should be to read through the
`sample application <./app/main.py>`_. That'll give you an overview of what
telemetry we'll get, how we instrument our applications, and some of the high
level goals.

From there, you should read through the
`application cluster spec <./appcluster.yaml>`_, which will introduce the
various methods of capturing and forwarding your telemetry.

Finally, you should read through the
`reporting cluster spec <./reportcluster.yaml>`_, which will handle all the
aggregation, reporting, and operations side of things.

If you're the type to appreciate a visual reference, you may also want to take
a look at the `architecture diagram <./architecture.png>`_.

To get an understanding of the useability, you can run ``make``. You'll need
to have docker running and your ``kubectl`` configured to point to a valid
cluster. I've not attempted to avoid causing issues with existing clusters;
please use a fresh cluster! ``make clean`` can tear down the changes when
you're done.

TODO: fix GCS reliance

Once the cluster is running, you can check out ``:3000`` for a Grafana instance
and explore the data. The user/pass is ``admin:admin``. You shouldn't need to
access anything else, but you can do so by port-forwarding to a given service
if you want to poke around. For example, to check out the ``alertmanager`` on
``appcluster-a``, you can run::

    kubectl port-forward -nappcluster-a-monitoring service/alertmanager 9093:9093
    # then visit localhost:9093

The above should be everything you need to know to understand what's going on
here. The rest of this README will discuss more orthogonal topics and design
decisions.

Why Prometheus?
---------------

Why Thanos?
-----------

Why Loki?
---------

Why Tempo?
----------

Why Grafana Agent?
------------------

Other "Why"'s?
--------------

TODO
----

* logs:
  * examplars?:
    * https://grafana.com/docs/grafana/latest/datasources/tempo/#trace-to-logs
    * https://grafana.com/blog/2021/03/31/intro-to-exemplars-which-enable-grafana-tempos-distributed-tracing-at-massive-scale/
  * promtail ready probe fix
  * ruler missing?
  * logcli integration:
    * https://grafana.com/docs/loki/latest/getting-started/logcli/ 
* traces:
  * consider using grafana-agent for prometheus/loki forwarding?
  * capturing all tags?:
    * https://grafana.com/blog/2020/11/17/tracing-with-the-grafana-agent-and-grafana-tempo/
* metrics:
  * investigate value of thanos query frontend
  * figure out grafana v8 ngalerts integration given thanos-query proxy usage
  * node-exporter and kube-state-metrics:
    * https://www.metricfire.com/blog/ha-kubernetes-monitoring-using-prometheus-and-thanos
* docs:
  * constant casing eg. of Prometheus
* ensure everything has a scrape config
* use port names
* verify everything!
