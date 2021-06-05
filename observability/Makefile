TAG:=$(shell date +%s)


all: deploy

build:
	docker build -t thekevjames/o11y-app:$(TAG) app

deploy: build
	kubectl apply -f k8s.yaml
	kubectl set image -ndefault deployment/app app=thekevjames/o11y-app:$(TAG)
