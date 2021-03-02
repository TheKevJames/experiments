import asyncio

import aiohttp
import typer

from .config import URL
from .utils import coro


app = typer.Typer()


@app.command()
@coro
async def run(count: int = 1, batch: int = 1) -> None:
    sema = asyncio.Semaphore(batch)

    async def get(s: aiohttp.ClientSession) -> bool:
        async with sema:
            resp = await s.get(URL)
            return resp.status == 200 and await resp.text() == 'OK\n'

    fails = 0
    conn = aiohttp.TCPConnector(limit=batch)
    async with aiohttp.ClientSession(connector=conn) as s:
        tasks = [get(s) for _ in range(count)]
        for task in asyncio.as_completed(tasks):
            fails += not await task

    assert fails == 0
