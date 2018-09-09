import aiohttp


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
