#!/usr/bin/env python
"""
Pub/Sub subscription sync

Usage:
  sink.py PROJECT SUBSCRIPTION
  sink.py -h | --help

Options:
  -h --help                show this screen
"""
import os
import time

import docopt
from google.cloud import pubsub


os.environ['PUBSUB_EMULATOR_HOST'] = '0.0.0.0:8681'

LAST = 0.


def callback(message) -> None:
    global LAST

    now = time.time()
    if now - LAST > 1:
        print('---')
    LAST = now

    print('.')
    message.ack()


def main(args: dict) -> None:
    subscriber = pubsub.SubscriberClient()
    subscription = f'projects/{args["PROJECT"]}/subscriptions/{args["SUBSCRIPTION"]}'
    future = subscriber.subscribe(subscription, callback)
    try:
        future.result()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main(docopt.docopt(__doc__))
