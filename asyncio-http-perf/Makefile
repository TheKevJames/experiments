UNAME := $(shell uname -s)
ifeq ($(UNAME),Linux)
	PROCS := $(shell nproc)
endif
ifeq ($(UNAME),Darwin)
	PROCS := $(shell sysctl -n hw.physicalcpu)
endif

all: README.rst

README.rst: README.src perf.rst
	cp $< $@
	echo '' >>$@
	cat $(word 2,$^) >>$@

perf.rst: perf.md
	sed -i 's/poetry run client //' $^
	pandoc -trst --wrap=none $< >$@

perf.md:
	hyperfine -w3 \
		--show-output \
		--export-json perf.json \
		--export-markdown $@ \
		-L client aiohttp,asks,httpx \
		'poetry run client {client} run --count=1 --batch=1' \
		'poetry run client {client} run --count=10 --batch=1' \
		'poetry run client {client} run --count=10 --batch=10' \
		'poetry run client {client} run --count=100 --batch=1' \
		'poetry run client {client} run --count=100 --batch=10' \
		'poetry run client {client} run --count=100 --batch=100' \
		'poetry run client {client} run --count=1000 --batch=1' \
		'poetry run client {client} run --count=1000 --batch=10' \
		'poetry run client {client} run --count=1000 --batch=100' \
		'poetry run client {client} run --count=1000 --batch=100'

# TODO:
# hub clone sharkdp/hyperfine ...
# modify (non-float)
# perf.png: perf.json
# 	python hyperfine/scripts/plot_parametrized.py -o perf.png perf.json

bench: clean perf.md

server:
	GOMAXPROCS=$(PROCS) go run server.go

clean:
	rm -f perf.* README.rst
