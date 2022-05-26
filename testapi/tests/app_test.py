import httpx


async def test_root(client: httpx.AsyncClient) -> None:
    response = await client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World!'}
