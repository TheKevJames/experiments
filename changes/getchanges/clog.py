import asyncio
import logging

import aiohttp

from .indexes import get


log = logging.getLogger(__name__)


class Clog:
    def __init__(self, raw: str, url: str) -> None:
        self.raw = raw
        self.url = url

    def __repr__(self) -> str:
        return self.raw

    @classmethod
    async def init(cls, url: str, *, session: aiohttp.ClientSession) -> 'Clog':
        resp = await session.get(url)
        resp.raise_for_status()
        raw = await resp.text()

        return cls(raw=raw, url=url)


async def retrieve(name: str, *, source: str = None,
                   session: aiohttp.ClientSession) -> Clog:
    futures = []
    for index in get():
        if source and source not in index.hints:
            continue

        futures.append(index.find_url(name, session=session))

    urls = {u for ul in await asyncio.gather(*futures) for u in ul if u}

    # TODO: return best rather than first
    for url in urls:
        return await Clog.init(url, session=session)

    log.error(f'could not find changelog for {name}')
