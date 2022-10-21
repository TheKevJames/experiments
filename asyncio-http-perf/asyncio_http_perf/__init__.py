import typer

from . import aiohttp
from . import httpx


app = typer.Typer()
app.add_typer(aiohttp.app, name='aiohttp')
app.add_typer(httpx.app, name='httpx')
