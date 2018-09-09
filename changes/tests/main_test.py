import aiohttp
import pytest

import changes


@pytest.mark.asyncio
async def test_coveralls():
    # PyPI project_urls -> GitHub:/CHANGELOG.md
    async with aiohttp.ClientSession() as s:
        clog = await changes.retrieve('coveralls', source='pypi', session=s)

    assert clog


@pytest.mark.asyncio
async def test_hypothesis():
    # PyPI info -> GitHub:/hypothesis-python -> ./docs/CHANGELOG.rst
    async with aiohttp.ClientSession() as s:
        clog = await changes.retrieve('hypothesis', source='pypi', session=s)

    assert clog


@pytest.mark.asyncio
async def test_pytest():
    # PyPI info -> GitHub:/ -> ./CHANGELOG.rst
    async with aiohttp.ClientSession() as s:
        clog = await changes.retrieve('pytest', source='pypi', session=s)

    assert clog
