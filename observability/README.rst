TODO
====

* node-exporter
* kube-state-metrics
* tweak resources
* grafana v8 ngalerts given thanos-query proxy
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

grafana at :3000
