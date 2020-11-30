#!/usr/bin/env python
"""
Pub/Sub publisher

Usage:
  push.py [--num=<num>] [--rate=<rate>] PROJECT TOPIC
  push.py -h | --help

Options:
  --num=<num>       number of pushes [default: 1]
  --rate=<rate>     rate of pushing [default: 1]
  -h --help         show this screen
"""
import grpc
import os

import docopt
from google.cloud import pubsub
from google.cloud.pubsub_v1.types import PubsubMessage
from google.cloud.pubsub_v1.gapic import publisher_client
from google.cloud.pubsub_v1.gapic.transports import publisher_grpc_transport


os.environ['PUBSUB_EMULATOR_HOST'] = '0.0.0.0:8681'


def batches(iterable, n=1):
    l = len(iterable)
    for i in range(0, l, n):
        yield iterable[i:min(i + n, l)]


def main(args: dict) -> None:
    # batch_settings = pubsub.types.BatchSettings(max_messages=10)
    # publisher = pubsub.PublisherClient(batch_settings=batch_settings)

    kwargs = {}
    emulator = os.environ.get('PUBSUB_EMULATOR_HOST')
    if emulator:
        channel = grpc.insecure_channel(target=emulator)
    else:
        channel = grpc_helpers.create_channel(credentials=None,
                                              target=publisher_client.PublisherClient.SERVICE_ADDRESS,
                                              scopes=publisher_client.PublisherClient._DEFAULT_SCOPES,
                                              options=[('grpc.max_send_message_length', -1),
                                                       ('grpc.max_receive_message_length', -1)])
    transport = publisher_grpc_transport.PublisherGrpcTransport(
        channel=channel)
    api = publisher_client.PublisherClient(transport=transport)

    topic = f'projects/{args["PROJECT"]}/topics/{args["TOPIC"]}'

    for xs in batches(range(int(args['--num'])), int(args['--rate'])):
        messages = []
        for x in xs:
            if x is None:
                break
            # message = PubsubMessage(data=b'foobar', ordering_key='', attributes={})
            message = PubsubMessage(data=b'foobar', attributes={})
            messages.append(message)
            print('.', end='')

        # retries, then raises google.api_core.exceptions.GoogleAPIError
        # response = publisher.api.publish(topic, messages)
        response = api.publish(topic, messages, retry=None, timeout=1)
        print()


# def main(args: dict) -> None:
#     batch_settings = pubsub.types.BatchSettings(max_messages=1)
#     publisher = pubsub.PublisherClient(batch_settings=batch_settings)
#     topic = f'projects/{args["PROJECT"]}/topics/{args["TOPIC"]}'
#     for _ in range(int(args['--num'])):
#         publisher.publish(topic, b'foobar')
#     publisher.stop()

if __name__ == '__main__':
    main(docopt.docopt(__doc__))
