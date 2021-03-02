all: README.rst

README.rst: README.src perf.rst
	cp $< $@
	echo '' >>$@
	cat $(word 2,$^) >>$@

perf.rst: perf.md
	sed -i 's/poetry run client //' $^
	pandoc -trst --wrap=none $< >$@

perf.md:
	hyperfine -w3 --export-markdown results.md \
		'poetry run client aiohttp run --count=1' \
		'poetry run client aiohttp run --count=10' \
		'poetry run client aiohttp run --count=100' \
		'poetry run client aiohttp run --count=100 --batch=10' \
		'poetry run client aiohttp run --count=100 --batch=100' \
		'poetry run client aiohttp run --count=1000' \
		'poetry run client aiohttp run --count=1000 --batch=10' \
		'poetry run client aiohttp run --count=1000 --batch=100' \
		'poetry run client asks run --count=1' \
		'poetry run client asks run --count=10' \
		'poetry run client asks run --count=100' \
		'poetry run client asks run --count=100 --batch=10' \
		'poetry run client asks run --count=100 --batch=100' \
		'poetry run client asks run --count=1000' \
		'poetry run client asks run --count=1000 --batch=10' \
		'poetry run client asks run --count=1000 --batch=100' \
		'poetry run client httpx run --count=1' \
		'poetry run client httpx run --count=10' \
		'poetry run client httpx run --count=100' \
		'poetry run client httpx run --count=100 --batch=10' \
		'poetry run client httpx run --count=100 --batch=100' \
		'poetry run client httpx run --count=1000' \
		'poetry run client httpx run --count=1000 --batch=10' \
		'poetry run client httpx run --count=1000 --batch=100'

bench: clean perf.md

server:
	GOMAXPROCS=$(shell nproc) go run server.go

clean:
	rm -f perf.* README.rst
