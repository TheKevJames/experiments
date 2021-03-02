import asyncio

import asks
import typer

from .config import URL
from .utils import coro


app = typer.Typer()


@app.command()
@coro
async def run(count: int = 1, batch: int = 1) -> None:
    sema = asyncio.Semaphore(batch)

    async def get(s: asks.Session) -> bool:
        async with sema:
            resp = await s.get(URL)
            return resp.status_code == 200 and resp.text == 'OK\n'

    fails = 0
    s = asks.Session(connections=batch)
    tasks = [get(s) for _ in range(count)]
    for task in asyncio.as_completed(tasks):
        fails += not await task

    assert fails == 0
