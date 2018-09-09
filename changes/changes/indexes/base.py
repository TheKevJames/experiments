import typing


class Base:
    hints: typing.Set[str] = {}

    @staticmethod
    async def find_url(name: str) -> str:
        raise NotImplementedError
