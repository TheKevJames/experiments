import logging
# Yes, we get it, Tensorflow v2.x is going to refactor everything.
logging.getLogger('tensorflow').setLevel(logging.ERROR)

from .predict import predict  # noqa


__all__ = ['predict']
