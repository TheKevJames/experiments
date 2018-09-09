"""changes

Usage:
    changes [options] NAME

Options:
    -s --source=SOURCE  Provide a source restriction.
    -h --help           Display this help.
"""
import asyncio
import logging
import sys

import aiohttp
import docopt

from .clog import Clog
from .indexes import get
from .version import __version__


log = logging.getLogger('changes')


async def main() -> None:
    args = docopt.docopt(__doc__, version=__version__)

    async with aiohttp.ClientSession() as session:
        futures = []
        for index in get():
            if args.get('--source') and args['--source'] not in index.hints:
                continue

            futures.append(index.find_url(args['NAME'], session=session))

        urls = {u for ul in await asyncio.gather(*futures) for u in ul if u}

        # TODO: return best
        for url in urls:
            clog = await Clog.init(url, session=session)
            print(clog)
            return

    log.error(f'could not find changelog for {args["NAME"]}')
    sys.exit(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
