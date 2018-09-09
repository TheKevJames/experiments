import asyncio
import os

import aiohttp

from .base import Base


TOKEN = os.environ.get('GITHUB_TOKEN')


class GitHub(Base):
    hints = {'github.com', 'githubusercontent.com'}

    @staticmethod
    def _headers() -> dict:
        h = {}
        if TOKEN:
            h['Authorization'] = f'token {TOKEN}'
        return h

    @classmethod
    async def _get(cls, owner: str, repo: str, route: str, *,
                   session: aiohttp.ClientSession) -> dict:
        url = f'https://api.github.com/repos/{owner}/{repo}/{route}'

        resp = await session.get(url, headers=cls._headers())
        resp.raise_for_status()
        return await resp.json()

    @classmethod
    async def _get_paths(cls, owner: str, repo: str, *, path: str = '',
                         session: aiohttp.ClientSession) -> dict:
        files = await cls._get(owner, repo, f'contents/{path}',
                               session=session)

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

        *_, owner, repo = url.strip('/').rsplit('/', 2)

        files = await cls._get_paths(owner, repo, path=path, session=session)
        if not files:
            releases = await cls._get(owner, repo, 'releases', session=session)
            # TODO: there doesn't seem to be a programatic way to get release
            # notes contents...
            return releases[0]['html_url']

        # TODO: pick best
        return cls.get_url(list(files)[0])

        # TODO: consider fallback to commit log

    @staticmethod
    def get_url(url: str) -> str:
        return url\
            .replace('github.com', 'raw.githubusercontent.com')\
            .replace('/blob', '')
