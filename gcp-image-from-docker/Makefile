bucket =

all: image-optimized

disk.tar: Dockerfile $(wildcard builtin/*)
	docker build -t gcpimg .
	docker create --name=gcpcont gcpimg
	docker export -o $@ gcpcont
	docker rm gcpcont

disk.img: disk.tar $(wildcard builtin/*) $(wildcard conf/*)
	docker run -it \
		-v $(shell pwd):/os:rw \
		--privileged \
		--cap-add SYS_ADMIN \
		--device /dev/loop0 \
		--device /dev/loop1 \
		gcpimg \
		bash /os/conf/configure.sh

disk.raw: disk.img
	qemu-img convert -O raw $< $@

disk.tar.gz: disk.raw
	gtar --format=oldgnu -Sczf $@ $<

ensure-bucket:
ifndef bucket
	$(error Please specify bucket name ("make bucket=my-bucket-for-vm-images"))
endif
	gsutil mb gs://$(bucket) || true

upload: disk.tar.gz ensure-bucket
	gsutil cp $< gs://$(bucket)

image-unoptimized: upload
	gcloud compute images create custom-unoptimized \
		--source-uri gs://$(bucket)/disk.tar.gz

image-optimized: image-unoptimized
	gcloud compute images import custom-v$(shell date '+%Y%m%d') \
		--source-image custom-unoptimized \
		--os debian-9
	yes | gcloud compute images delete custom-unoptimized

clean:
	cat .dockerignore | xargs rm -rf
