TAG:=$(shell date +%s)


all: deploy

build:
	docker build -t thekevjames/o11y-app:$(TAG) appcluster/app
	docker build -t thekevjames/o11y-prometheus:$(TAG) appcluster/prometheus
	docker build -t thekevjames/o11y-alertmanager:$(TAG) appcluster/alertmanager
	docker build -t thekevjames/o11y-grafana:$(TAG) reportcluster/grafana

deploy: build
	kubectl apply -f k8s/
	kubectl set image -n appcluster-a-default deployment/app app=thekevjames/o11y-app:$(TAG)
	kubectl set image -n appcluster-b-default deployment/app app=thekevjames/o11y-app:$(TAG)
	kubectl set image -n appcluster-a-monitoring deployment/prometheus prometheus=thekevjames/o11y-prometheus:$(TAG)
	kubectl set image -n appcluster-b-monitoring deployment/prometheus prometheus=thekevjames/o11y-prometheus:$(TAG)
	kubectl set image -n appcluster-a-monitoring deployment/alertmanager alertmanager=thekevjames/o11y-alertmanager:$(TAG)
	kubectl set image -n appcluster-b-monitoring deployment/alertmanager alertmanager=thekevjames/o11y-alertmanager:$(TAG)
	kubectl set image -n reportcluster-a-monitoring deployment/grafana grafana=thekevjames/o11y-grafana:$(TAG)
