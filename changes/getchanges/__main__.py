"""changes

Usage:
    changes [options] NAME

Options:
    -s --source=SOURCE  Provide a source restriction.
    -h --help           Display this help.
"""
import asyncio
import sys

import aiohttp
import docopt

from .clog import retrieve
from .version import __version__


async def run() -> None:
    args = docopt.docopt(__doc__, version=__version__)

    name = args['NAME']
    source = args.get('--source')
    async with aiohttp.ClientSession() as session:
        clog = await retrieve(name, source=source, session=session)

    if not clog:
        sys.exit(1)

    print(clog)


def main() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


if __name__ == '__main__':
    main()
