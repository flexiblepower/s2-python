import abc
import asyncio
from asyncio import AbstractEventLoop
import typing
from typing import AsyncGenerator, Union

from s2python.s2_parser import UnparsedS2Message


class S2MediumException(Exception):
    ...

class MediumClosedConnectionError(S2MediumException):
    ...

class MediumCouldNotConnectError(S2MediumException):
    ...


class S2AsyncMediumConnection(abc.ABC):
    @abc.abstractmethod
    async def is_connected(self) -> bool:
        ...

    @abc.abstractmethod
    async def messages(self) -> AsyncGenerator[UnparsedS2Message, None]:
        ...

    @abc.abstractmethod
    async def send(self, message: str) -> None:
        ...


class S2SyncMediumConnection(abc.ABC):
    @abc.abstractmethod
    def is_connected(self) -> bool:
        ...

    @abc.abstractmethod
    def messages(self) -> typing.Generator[UnparsedS2Message, None, None]:
        ...

    @abc.abstractmethod
    def send(self, message: str) -> None:
        ...


S2MediumConnection = Union[S2AsyncMediumConnection, S2SyncMediumConnection]


class S2SyncToAsyncMediumConnection(S2AsyncMediumConnection):
    _sync_medium: S2SyncMediumConnection
    _eventloop: AbstractEventLoop

    def __init__(self, sync_medium: S2SyncMediumConnection, eventloop: typing.Optional[AbstractEventLoop] = None) -> None:
        self._sync_medium = sync_medium
        self._eventloop = asyncio.get_event_loop() if eventloop is None else eventloop

    async def is_connected(self) -> bool:
        return await self._eventloop.run_in_executor(None, self._sync_medium.is_connected)

    async def messages(self) -> AsyncGenerator[UnparsedS2Message, None]:
        generator = await self._eventloop.run_in_executor(None, self._sync_medium.messages)

        while True:
            yield await self._eventloop.run_in_executor(None, generator.__next__)

    async def send(self, message: str) -> None:
        await self._eventloop.run_in_executor(None, self._sync_medium.send, message)
