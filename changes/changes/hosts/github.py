import asyncio

import aiohttp

from .base import Base


FILENAMES = {'changes', 'changelog'}


class GitHub(Base):
    hints = {'github.com', 'githubusercontent.com'}

    @staticmethod
    def _to_canonical_url(url: str) -> str:
        return url\
            .replace('github.com', 'raw.githubusercontent.com')\
            .replace('/blob', '')

    @classmethod
    async def _get_paths(cls, owner: str, repo: str, *, path: str = '',
                         session=aiohttp.ClientSession) -> dict:
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

        resp = await session.get(url)
        resp.raise_for_status()
        files = await resp.json()

        futures = []
        for folder in {f['path'] for f in files if f['type'] == 'dir'}:
            if any(folder.replace(path, '').strip('/').startswith(x)
                   for x in {'change', 'doc'}):
                futures.append(cls._get_paths(owner, repo, path=folder,
                                              session=session))

        filemap = {f['html_url']: f['name'].lower() for f in files
                   if f['type'] == 'file'}
        [filemap.update(f) for f in await asyncio.gather(*futures)]

        return {url: name for url, name in filemap.items()
                if any(name.startswith(x) for x in {'changelog', 'changes'})}

    @classmethod
    async def find_clog(cls, url: str, *,
                        session=aiohttp.ClientSession) -> str:
        if '/tree/master/' in url:
            url, path = url.split('/tree/master/')
        else:
            path = ''

        *_, owner, repo = url.rsplit('/', 2)

        files = await cls._get_paths(owner, repo, path=path, session=session)
        # TODO: pick best
        return cls._to_canonical_url(list(files)[0])
