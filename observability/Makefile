TAG:=$(shell date +%s)


all: deploy

build:
	docker build -t thekevjames/o11y-app:$(TAG) app
	docker build -t thekevjames/o11y-prometheus:$(TAG) prometheus
	docker build -t thekevjames/o11y-alertmanager:$(TAG) alertmanager
	docker build -t thekevjames/o11y-grafana:$(TAG) grafana

deploy: build
	kubectl apply -f k8s.yaml
	kubectl set image -ndefault deployment/app app=thekevjames/o11y-app:$(TAG)
	kubectl set image -nmonitoring deployment/prometheus prometheus=thekevjames/o11y-prometheus:$(TAG)
	kubectl set image -nmonitoring deployment/alertmanager alertmanager=thekevjames/o11y-alertmanager:$(TAG)
	kubectl set image -nmonitoring deployment/grafana grafana=thekevjames/o11y-grafana:$(TAG)
