#!/usr/bin/env python
"""
Google Pub/Sub Performance Test Harness

Usage:
  run.py [--rate=<rate>] [--duration=<duration>] [--style=<style>]
  run.py -h | --help

Options:
  --duration=<duration>    duration of test in seconds [default: 10]
  --rate=<rate>            per second publish rate [default: 1]
  --style=<style>          pull style (async | sync) [default: async]
  -h --help                show this screen
"""
import concurrent.futures
import datetime
import functools
import multiprocessing
import multiprocessing.sharedctypes
import os
import statistics
import subprocess
import time

import docopt
import numpy  # I guess I should upgrade to py3.8...
from google.cloud import pubsub


PROJECT = subprocess.run(['gcloud', 'config', 'get-value', 'project'],
                         capture_output=True).stdout.decode().strip()
TOPIC = 'thekevjames-test-perf'


def setup():
    publisher = pubsub.PublisherClient()
    topic = f'projects/{PROJECT}/topics/{TOPIC}'
    try:
        publisher.create_topic(topic)
    except Exception:
        pass

    subscriber = pubsub.SubscriberClient()
    subscription = f'projects/{PROJECT}/subscriptions/{TOPIC}-0'
    try:
        subscriber.create_subscription(name=subscription, topic=topic)
    except Exception:
        pass


def print_stats(local: list, server: list, *, duration: int, rate: int):
    print(f'Total Items: {rate}x{duration} => {len(local)}')
    if len(local) != duration * rate:
        print('    \033[91m> Mismatched Results!\033[0m')
    print()

    print(f'Mean from Process: {statistics.mean(local):.4f}')
    arr = numpy.array(local)
    print(f'50th from Process: {numpy.percentile(arr, 50):.4f}')
    print(f'75th from Process: {numpy.percentile(arr, 75):.4f}')
    print(f'85th from Process: {numpy.percentile(arr, 85):.4f}')
    print(f'95th from Process: {numpy.percentile(arr, 95):.4f}')
    print(f'99th from Process: {numpy.percentile(arr, 99):.4f}')

    print()

    print(f'Mean from Server: {statistics.mean(server):.4f}')
    arr = numpy.array(server)
    print(f'50th from Server: {numpy.percentile(arr, 50):.4f}')
    print(f'75th from Server: {numpy.percentile(arr, 75):.4f}')
    print(f'85th from Server: {numpy.percentile(arr, 85):.4f}')
    print(f'95th from Server: {numpy.percentile(arr, 95):.4f}')
    print(f'99th from Server: {numpy.percentile(arr, 99):.4f}')


def publish(*, duration: int, rate: int):
    publisher = pubsub.PublisherClient(
        batch_settings=pubsub.types.BatchSettings(max_messages=rate))
    topic = f'projects/{PROJECT}/topics/{TOPIC}'

    for _ in range(duration):
        start = time.perf_counter()
        for _ in range(rate):
            publisher.publish(topic, b'test message payload',
                              timestamp=str(time.time()).encode())
        end = time.perf_counter()
        try:
            time.sleep(1 - (end - start))
        except ValueError:
            print('\033[91mPublishing too slowly -- add more threads!\033[0m')
        # else:
        #     print(f'Published {rate} items in {end - start:.4f}s')

    publisher.stop()


def callback(local, server, message):
    now = time.time()

    local_latency = round(now - float(message.attributes['timestamp']), 4)
    local.append(local_latency)

    try:
        # async
        server_latency = round(now - message.publish_time.timestamp(), 4)
        server.append(server_latency)
    except AttributeError:
        # sync, ie. protobufs
        epoch = (message.publish_time.seconds
                 + message.publish_time.nanos / (10 ** 9))
        server_latency = round(now - epoch, 4)
        server.append(server_latency)

    try:
        # async
        message.ack()
    except AttributeError:
        # sync, ie. protobufs
        pass


def subscribe_async(latencies_local, latencies_server, *, count: int,
                    duration: int, rate: int):
    subscriber = pubsub.SubscriberClient()
    topic = f'projects/{PROJECT}/topics/{TOPIC}'
    subscription = f'projects/{PROJECT}/subscriptions/{TOPIC}-0'

    cb = functools.partial(callback, latencies_local, latencies_server)
    future = subscriber.subscribe(subscription, cb)
    try:
        future.result(timeout=duration + 5)
    except concurrent.futures.TimeoutError:
        pass


def subscribe_sync(latencies_local, latencies_server, *, count: int,
                   duration: int, rate: int):
    subscriber = pubsub.SubscriberClient()
    subscription = f'projects/{PROJECT}/subscriptions/{TOPIC}-0'

    for _ in range(duration * rate // count):
        # theoretically, timeout should only apply on the first message, eg.
        # since we are still spinning up `fn_count` processes...
        response = subscriber.pull(subscription, max_messages=1, timeout=100)
        for msg in response.received_messages:
            callback(latencies_local, latencies_server, msg.message)

        ack_ids = [msg.ack_id for msg in response.received_messages]
        subscriber.acknowledge(subscription, ack_ids)


def main(args: dict):
    setup()

    duration = int(args['--duration'])
    rate = int(args['--rate'])
    (fn, fn_count) = {
        'async': (subscribe_async, 1),
        'sync': (subscribe_sync, -(-rate // 10)),
    }[args['--style']]

    # lest I have to do more complicated math
    assert not duration * rate % fn_count, 'Invalid subscriber thread count'

    manager = multiprocessing.Manager()
    latencies_local = manager.list()
    latencies_server = manager.list()

    ps = []
    for _ in range(fn_count):
        p = multiprocessing.Process(target=fn,
                                    args=(latencies_local, latencies_server),
                                    kwargs={'count': fn_count,
                                            'duration': duration,
                                            'rate': rate})
        p.start()
        ps.append(p)

    publish(duration=duration, rate=rate)

    _ = [p.join() for p in ps]
    print_stats(latencies_local, latencies_server, duration=duration,
                rate=rate)


if __name__ == '__main__':
    main(docopt.docopt(__doc__))
