import typing

from .base import Base
from .pypi import PyPI


def get() -> typing.Set[Base]:
    return {PyPI}


__all__ = ['get']
