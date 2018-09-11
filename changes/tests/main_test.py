import aiohttp
import pytest

import getchanges


@pytest.mark.asyncio
async def test_alabaster():
    # PyPI project_urls -> RtD:/ -> ./changelog.html
    async with aiohttp.ClientSession() as s:
        clog = await getchanges.retrieve('alabaster', source='pypi', session=s)

    assert clog


@pytest.mark.asyncio
async def test_coveralls():
    # PyPI project_urls -> GitHub:/CHANGELOG.md
    async with aiohttp.ClientSession() as s:
        clog = await getchanges.retrieve('coveralls', source='pypi', session=s)

    assert clog


@pytest.mark.asyncio
async def test_gcloud_rest():
    # PyPI info -> GitHub:/ -> GitHub Releases
    async with aiohttp.ClientSession() as s:
        clog = await getchanges.retrieve('gcloud-rest', source='pypi',
                                         session=s)

    assert clog


@pytest.mark.asyncio
async def test_hypothesis():
    # PyPI info -> GitHub:/hypothesis-python -> ./docs/CHANGELOG.rst
    async with aiohttp.ClientSession() as s:
        clog = await getchanges.retrieve('hypothesis', source='pypi',
                                         session=s)

    assert clog


@pytest.mark.asyncio
async def test_pytest():
    # PyPI info -> GitHub:/ -> ./CHANGELOG.rst
    async with aiohttp.ClientSession() as s:
        clog = await getchanges.retrieve('pytest', source='pypi', session=s)

    assert clog
