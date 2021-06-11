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

clean: clean-for-deploy
	kubectl get service --all-namespaces \
		| grep -v '^default' | grep -v '^kube-node-lease' | grep -v '^kube-public' | grep -v '^kube-system' | grep -v 'NAMESPACE' \
		| awk '{print "-n" $$1, $$2}' \
		| xargs -n2 kubectl delete service
	kubectl get deployment --all-namespaces \
		| grep -v '^default' | grep -v '^kube-node-lease' | grep -v '^kube-public' | grep -v '^kube-system' | grep -v 'NAMESPACE' \
		| awk '{print "-n" $$1, $$2}' \
		| xargs -n2 kubectl delete deployment
	kubectl get configmap --all-namespaces \
		| grep -v '^default' | grep -v '^kube-node-lease' | grep -v '^kube-public' | grep -v '^kube-system' | grep -v 'NAMESPACE' \
		| awk '{print "-n" $$1, $$2}' \
		| xargs -n2 kubectl delete configmap
	kubectl get secret --all-namespaces \
		| grep -v '^default' | grep -v '^kube-node-lease' | grep -v '^kube-public' | grep -v '^kube-system' | grep -v 'NAMESPACE' \
		| awk '{print "-n" $$1, $$2}' \
		| xargs -n2 kubectl delete secret
	kubectl delete ns \
		appcluster-a-default appcluster-a-monitoring \
		appcluster-b-default appcluster-b-monitoring \
		reportcluster-a-monitoring ||:
