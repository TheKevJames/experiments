import logging

import aiohttp


log = logging.getLogger(__name__)


class PyPI:
    sources = {'pip', 'pypi', 'py', 'python'}

    @classmethod
    async def lookup(cls, name: str, *, session=aiohttp.ClientSession) -> str:
        try:
            pypi_url = f'https://pypi.org/pypi/{name}/json'
            resp = await session.get(pypi_url)
            resp.raise_for_status()
            metadata = await resp.json()

            project_urls = metadata.get('info', {}).get('project_urls', {})
            for k in {'changes', 'Changes', 'changelog', 'Changelog'}:
                if project_urls.get(k):
                    return project_urls[k]

            for k in {'source', 'Source', 'repo', 'Repo'}:
                if project_urls.get(k):
                    # TODO: return await Github.lookup(project_urls[k])
                    raise NotImplementedError

            # TODO: return await Github.lookup(metadata['home_page'])
            raise NotImplementedError
        except Exception as e:
            log.error(f'could not find PyPI changelog for {name}', exc_info=e)
            raise
