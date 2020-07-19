#!/usr/bin/env python3
import cffi


builder = cffi.FFI()
builder.cdef('int fib(int n);')
builder.set_source('_lib_cffi',
                   '#include "lib.h"',
                   sources=['./lib/nimcache/lib.c', './lib/nimcache/stdlib_system.c'],
                   include_dirs=['/usr/lib/nim', './lib/nimcache'])


if __name__ == '__main__':
    builder.compile(verbose=True)
