import asyncio
import functools


def coro(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return inner
