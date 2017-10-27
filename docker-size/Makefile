all: alpine alpine-multi alpine-multi-from-standard alpine-remove-deps standard standard-multi

test:
	@echo -n 'Alpine:                             '
	@docker run --rm -it thekevjames/experiments:alpine

	@echo -n 'Alpine (w/ deleted deps):           '
	@docker run --rm -it thekevjames/experiments:alpine-remove-deps

	@echo -n 'Alpine (Multi-Stage):               '
	@docker run --rm -it thekevjames/experiments:alpine-multi

	@echo -n 'Alpine (Multi-Stage from Standard): '
	@docker run --rm -it thekevjames/experiments:alpine-multi-from-standard

	@echo -n 'Standard:                           '
	@docker run --rm -it thekevjames/experiments:standard

	@echo -n 'Standard (Multi-Stage):             '
	@docker run --rm -it thekevjames/experiments:standard-multi

print:
	@echo -n 'Alpine:                             '
	@docker images --filter "reference=thekevjames/experiments:alpine" --format "{{.Size}}"

	@echo -n 'Alpine (w/ deleted deps):           '
	@docker images --filter "reference=thekevjames/experiments:alpine-remove-deps" --format "{{.Size}}"

	@echo -n 'Alpine (Multi-Stage):               '
	@docker images --filter "reference=thekevjames/experiments:alpine-multi" --format "{{.Size}}"

	@echo -n 'Alpine (Multi-Stage from Standard): '
	@docker images --filter "reference=thekevjames/experiments:alpine-multi-from-standard" --format "{{.Size}}"

	@echo -n 'Standard:                           '
	@docker images --filter "reference=thekevjames/experiments:standard" --format "{{.Size}}"

	@echo -n 'Standard (Multi-Stage):             '
	@docker images --filter "reference=thekevjames/experiments:standard-multi" --format "{{.Size}}"


.PHONY: alpine
alpine: alpine/requirements.txt alpine/script.py
	docker build -t thekevjames/experiments:alpine alpine/

.PHONY: alpine-multi
alpine-multi: alpine-multi/requirements.txt alpine-multi/script.py
	docker build -t thekevjames/experiments:alpine-multi alpine-multi/

.PHONY: alpine-multi-from-standard
alpine-multi-from-standard: alpine-multi-from-standard/requirements.txt alpine-multi-from-standard/script.py
	docker build -t thekevjames/experiments:alpine-multi-from-standard alpine-multi-from-standard/

.PHONY: alpine-remove-deps
alpine-remove-deps: alpine-remove-deps/requirements.txt alpine-remove-deps/script.py
	docker build -t thekevjames/experiments:alpine-remove-deps alpine-remove-deps/

.PHONY: standard
standard: standard/requirements.txt standard/script.py
	docker build -t thekevjames/experiments:standard standard/

.PHONY: standard-multi
standard-multi: standard-multi/requirements.txt standard-multi/script.py
	docker build -t thekevjames/experiments:standard-multi standard-multi/

alpine/requirements.txt: requirements.txt
	cp $^ $@
alpine/script.py: script.py
	cp $^ $@
alpine-multi/requirements.txt: requirements.txt
	cp $^ $@
alpine-multi/script.py: script.py
	cp $^ $@
alpine-multi-from-standard/requirements.txt: requirements.txt
	cp $^ $@
alpine-multi-from-standard/script.py: script.py
	cp $^ $@
alpine-remove-deps/requirements.txt: requirements.txt
	cp $^ $@
alpine-remove-deps/script.py: script.py
	cp $^ $@
standard/requirements.txt: requirements.txt
	cp $^ $@
standard/script.py: script.py
	cp $^ $@
standard-multi/requirements.txt: requirements.txt
	cp $^ $@
standard-multi/script.py: script.py
	cp $^ $@


clean:
	rm -f */requirements.txt
	rm -f */script.py

	docker rmi thekevjames/experiments:alpine
	docker rmi thekevjames/experiments:alpine-multi
	docker rmi thekevjames/experiments:alpine-multi-from-standard
	docker rmi thekevjames/experiments:alpine-remove-deps
	docker rmi thekevjames/experiments:standard
	docker rmi thekevjames/experiments:standard-multi
