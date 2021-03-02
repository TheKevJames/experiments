import typer

from . import aiohttp
from . import asks
from . import httpx


app = typer.Typer()
app.add_typer(aiohttp.app, name='aiohttp')
app.add_typer(asks.app, name='asks')
app.add_typer(httpx.app, name='httpx')
