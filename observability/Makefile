TAG:=$(shell date +%s)
USER?=o11y@thekev.in


all: deploy

build:
	docker build -t thekevjames/o11y-app:$(TAG) appcluster/app
	docker build -t thekevjames/o11y-alertmanager:$(TAG) appcluster/alertmanager
	docker build -t thekevjames/o11y-grafana:$(TAG) reportcluster/grafana

clean-for-deploy:
	kubectl delete secret -n appcluster-a-monitoring thanos-gcs-creds |:
	kubectl delete secret -n appcluster-b-monitoring thanos-gcs-creds |:
	kubectl delete secret -n reportcluster-a-monitoring thanos-gcs-creds |:

deploy: build clean-for-deploy
	kubectl apply -f k8s/
	kubectl create secret generic thanos-gcs-creds \
		-n appcluster-a-monitoring \
		--from-file=$(HOME)/.config/gcloud/legacy_credentials/$(USER)/adc.json
	kubectl create secret generic thanos-gcs-creds \
		-n appcluster-b-monitoring \
		--from-file=$(HOME)/.config/gcloud/legacy_credentials/$(USER)/adc.json
	kubectl create secret generic thanos-gcs-creds \
		-n reportcluster-a-monitoring \
		--from-file=$(HOME)/.config/gcloud/legacy_credentials/$(USER)/adc.json
	kubectl set image -n appcluster-a-default deployment/app app=thekevjames/o11y-app:$(TAG)
	kubectl set image -n appcluster-b-default deployment/app app=thekevjames/o11y-app:$(TAG)
	kubectl set image -n appcluster-a-monitoring deployment/alertmanager alertmanager=thekevjames/o11y-alertmanager:$(TAG)
	kubectl set image -n appcluster-b-monitoring deployment/alertmanager alertmanager=thekevjames/o11y-alertmanager:$(TAG)
	kubectl set image -n reportcluster-a-monitoring deployment/alertmanager alertmanager=thekevjames/o11y-alertmanager:$(TAG)
	kubectl set image -n reportcluster-a-monitoring deployment/grafana grafana=thekevjames/o11y-grafana:$(TAG)
