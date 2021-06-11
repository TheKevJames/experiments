TODO
====

* grafana v8, federated alerts
* node-exporter
* kube-state-metrics
* dashboards -> recording rules?
* backfill alerts from https://github.com/thanos-io/thanos/blob/main/examples/alerts/alerts.md:
  * or, probably, sample a couple as a minimal example
* tweak resources
* thanos query frontend?
* log stack
* trace stack
* grafana auth

READMEify Me
------------

Explain ns -> clusters
What corresponds to what, maybe break apart k8s files
Full walkthrough and reasoning for tech choices and location placement
make USER=foo

kubectl port-forward -nappcluster-a-monitoring service/alertmanager 9093:9093
kubectl port-forward -nreportcluster-a-monitoring service/thanos-ruler 9093:9093

kubectl port-forward -nreportcluster-a-monitoring service/thanos-querier 9090:9090

kubectl port-forward -nreportcluster-a-monitoring service/grafana 3000:3000
