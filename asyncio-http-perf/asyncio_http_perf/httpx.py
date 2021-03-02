import asyncio

import httpx
import typer

from .config import URL
from .utils import coro


app = typer.Typer()


@app.command()
@coro
async def run(count: int = 1, batch: int = 1) -> None:
    sema = asyncio.Semaphore(batch)

    async def get(s: httpx.AsyncClient) -> bool:
        async with sema:
            resp = await s.get(URL)
            return resp.status_code == 200 and resp.text == 'OK\n'

    fails = 0
    limits = httpx.Limits(max_keepalive_connections=batch,
                          max_connections=batch)
    async with httpx.AsyncClient(limits=limits) as s:
        tasks = [get(s) for _ in range(count)]
        for task in asyncio.as_completed(tasks):
            fails += not await task

    assert fails == 0
