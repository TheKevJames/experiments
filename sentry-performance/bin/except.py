import os
import statistics
import time


NUM_TESTS = int(os.environ['NUM_TESTS'])


def tests(count):
    for _ in range(count):
        start = time.perf_counter()
        try:
            raise ValueError('this is an exception')
        except ValueError:
            pass
        end = time.perf_counter()

        yield end - start


if __name__ == '__main__':
    times = list(tests(NUM_TESTS))

    print('Average: {:.12f}ms'.format(statistics.mean(times) * 1000))
    print('Median:  {:.12f}ms'.format(statistics.median(times) * 1000))
    print('Min:     {:.12f}ms'.format(min(times) * 1000))
    print('Max:     {:.12f}ms'.format(max(times) * 1000))
