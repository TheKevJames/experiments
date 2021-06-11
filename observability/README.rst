TODO
====

* thanos
  * set explicit prometheus retention, tweak resources
  * dedupe by replica label
* dashboards -> recording rules?
* log stack
* trace stack
* grafana auth

READMEify Me
------------

Explain ns -> clusters
What corresponds to what, maybe break apart k8s files

kubectl port-forward -nappcluster-a-monitoring service/prometheus 9090:9090
kubectl port-forward -nreportcluster-a-monitoring service/grafana 3000:3000
