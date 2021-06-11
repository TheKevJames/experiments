TODO
====

* logs:
  * json parser
  * handle dynamic ``extra`` values
  * examplars?
* traces
* metrics:
  * investigate value of thanos query frontend
  * figure out grafana v8 ngalerts integration given thanos-query proxy usage
  * node-exporter and kube-state-metrics:
    * https://www.metricfire.com/blog/ha-kubernetes-monitoring-using-prometheus-and-thanos
  * determine ideal resource configs
  * configure grafana auth
* misc:
  * see promtail: matchLabels run->name

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
