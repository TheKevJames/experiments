.PHONY: app bench clean lib venv
CC = clang
INC = -I/usr/lib/nim -I./lib/nimcache
LIBC = lib/nimcache/*.c
LIBCFFI = _lib_cffi.*.so
LIBJS = lib/nimcache/lib.js
LIBSO = lib/nimcache/lib.so

bench: app venv
	. venv/bin/activate; PYTHONPATH=$(shell pwd) hyperfine -w3 ./app/app.o ./app/app.ctypes.py ./app/app.cffi.py
app: app/app.o lib
lib: $(LIBC) $(LIBCFFI) $(LIBJS) $(LIBSO)
venv: venv/lib/python3.6/site-packages/cffi

%.o: %.c $(LIBC)
	$(CC) -O2 -o $@ $(INC) $^

$(LIBC): lib/lib.nim
	nim c --noMain --noLinking -d:release --opt:speed --header $<

$(LIBCFFI): $(LIBC) venv
	. venv/bin/activate; ./ffibuild.py

$(LIBJS): lib/lib.nim
	nim js --noMain --noLinking -d:release --opt:speed -o:$@ $<

$(LIBSO): $(LIBC)
	$(CC) -O2 -fPIC -shared -o $@ $(INC) $^

venv/bin/activate:
	python3 -m venv venv

venv/lib/python3.6/site-packages/cffi: venv/bin/activate
	. venv/bin/activate; pip install cffi

clean:
	find -iname "*.pyc" -delete
	rm -rf _lib_cffi.*
	rm -rf app/app.o
	rm -rf lib/nimcache
	rm -rf venv
