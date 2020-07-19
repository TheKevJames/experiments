#!/usr/bin/env python3
import ctypes


libmodule = ctypes.CDLL('./lib/nimcache/lib.so')


if __name__ == '__main__':
    for i in range(1, 40):
        print(f'fib({i}) = {libmodule.fib(i)}')
