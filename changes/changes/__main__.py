"""changes

Usage:
    changes [options] NAME

Options:
    -s --source=SOURCE  Provide a source restriction.
    -h --help           Display this help.
"""
import asyncio

import aiohttp
import docopt

from . import __version__
from .clog import Clog
from .sources import PyPI


async def main() -> None:
    args = docopt.docopt(__doc__, version=__version__)

    if args.get('--source'):
        if args['--source'] in PyPI.sources:
            async with aiohttp.ClientSession() as session:
                url = await PyPI.lookup(args['NAME'], session=session)
                clog = Clog(url)
                await clog.init(session=session)
                print(clog)
                return

    raise NotImplementedError


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
