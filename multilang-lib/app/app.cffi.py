#!/usr/bin/env python3
from _lib_cffi import lib


if __name__ == '__main__':
    for i in range(1, 40):
        print(f'fib({i}) = {lib.fib(i)}')
