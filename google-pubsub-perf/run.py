#!/usr/bin/env python
"""
Google Pub/Sub Performance Test Harness

Usage:
  run.py [--rate=<rate>] [--duration=<duration>]
  run.py -h | --help

Options:
  --duration=<duration>     duration of test in seconds [default: 10]
  --rate=<rate>             per second publish rate [default: 1]
  -h --help                 show this screen
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


def subscribe_async(*, duration: int, rate: int):
    subscriber = pubsub.SubscriberClient()
    topic = f'projects/{PROJECT}/topics/{TOPIC}'
    subscription = f'projects/{PROJECT}/subscriptions/{TOPIC}-0'

    manager = multiprocessing.Manager()
    latencies_local = manager.list()
    latencies_server = manager.list()

    def callback(local, server, message):
        now = time.time()

        local_latency = round(now - float(message.attributes['timestamp']), 4)
        local.append(local_latency)

        server_latency = round(now - message.publish_time.timestamp(), 4)
        server.append(server_latency)

        message.ack()

    cb = functools.partial(callback, latencies_local, latencies_server)
    future = subscriber.subscribe(subscription, cb)
    try:
        future.result(timeout=duration + 5)
    except concurrent.futures.TimeoutError:
        pass

    print(f'Total Items: {rate}x{duration} => {len(latencies_local)}')
    if len(latencies_local) != duration * rate:
        print('    \033[91m> Mismatched Results!\033[0m')
    print()

    print(f'Mean from Process: {statistics.mean(latencies_local):.4f}')
    arr = numpy.array(latencies_local)
    print(f'50th from Process: {numpy.percentile(arr, 50):.4f}')
    print(f'75th from Process: {numpy.percentile(arr, 75):.4f}')
    print(f'85th from Process: {numpy.percentile(arr, 85):.4f}')
    print(f'95th from Process: {numpy.percentile(arr, 95):.4f}')
    print(f'99th from Process: {numpy.percentile(arr, 99):.4f}')

    print()

    print(f'Mean from Server: {statistics.mean(latencies_server):.4f}')
    arr = numpy.array(latencies_server)
    print(f'50th from Server: {numpy.percentile(arr, 50):.4f}')
    print(f'75th from Server: {numpy.percentile(arr, 75):.4f}')
    print(f'85th from Server: {numpy.percentile(arr, 85):.4f}')
    print(f'95th from Server: {numpy.percentile(arr, 95):.4f}')
    print(f'99th from Server: {numpy.percentile(arr, 99):.4f}')


def main(args: dict):
    # setup()

    duration = int(args['--duration'])
    rate = int(args['--rate'])

    p = multiprocessing.Process(target=subscribe_async,
                                kwargs={'duration': duration, 'rate': rate})
    p.start()
    publish(duration=duration, rate=rate)
    p.join()


if __name__ == '__main__':
    main(docopt.docopt(__doc__))
