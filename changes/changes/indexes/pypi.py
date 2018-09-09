import asyncio
import logging
import typing

import aiohttp

from .base import Base
from ..hosts import find_clog


log = logging.getLogger(__name__)


class PyPI(Base):
    hints = {'pip', 'pypi', 'py', 'python'}

    @staticmethod
    async def find_url(name: str, *,
                       session=aiohttp.ClientSession) -> typing.Set[str]:
        candidates: typing.Set[str] = set()
        pypi_url = f'https://pypi.org/pypi/{name}/json'

        try:
            resp = await session.get(pypi_url)
            resp.raise_for_status()
            metadata = await resp.json()

            info = metadata.get('info', {})
            # TODO: metadata.get('releases') ?
            project_urls = info.get('project_urls', {})

            for k in {'changes', 'Changes', 'changelog', 'Changelog'}:
                if project_urls.get(k):
                    candidates.add(project_urls[k])

            repos = {info['home_page']}
            for k in {'source', 'Source', 'repo', 'Repo'}:
                if project_urls.get(k):
                    repos.add(project_urls[k])

            futures = [find_clog(r, session=session) for r in repos]
            candidates.update(set(await asyncio.gather(*futures)))
        except Exception as e:
            log.warning(f'could not find {name} on PyPI', exc_info=e)

        return candidates
