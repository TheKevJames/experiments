import aiohttp


class Clog:
    def __init__(self, url: str) -> None:
        self.raw = None
        # TODO: de-github in GH class
        self.url = url.replace(
            'github.com', 'raw.githubusercontent.com').replace('/blob', '')

    def __repr__(self) -> str:
        return self.raw

    async def init(self, *, session: aiohttp.ClientSession) -> None:
        resp = await session.get(self.url)
        resp.raise_for_status()
        self.raw = await resp.text()
