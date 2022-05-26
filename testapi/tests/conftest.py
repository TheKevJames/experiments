import httpx
import pytest

from testapi.app import app


@pytest.fixture(scope='function')
async def client() -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=app, base_url='http://test') as c:
        yield c
