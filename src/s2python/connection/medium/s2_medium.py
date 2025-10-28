import abc
from typing import AsyncGenerator

from s2python.s2_parser import UnparsedS2Message


class S2MediumException(Exception):
    ...

class MediumClosedConnectionError(S2MediumException):
    ...

class MediumCouldNotConnectError(S2MediumException):
    ...


class S2Medium(abc.ABC):
    @abc.abstractmethod
    async def connect(self) -> None:
        ...

    @abc.abstractmethod
    async def is_connected(self) -> bool:
        ...

    @abc.abstractmethod
    async def messages(self) -> AsyncGenerator[UnparsedS2Message, None]:
        ...

    @abc.abstractmethod
    async def send(self, message: str) -> None:
        ...

    @abc.abstractmethod
    async def close(self) -> None:
        ...