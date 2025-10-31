import abc
import typing
from typing import AsyncGenerator, Awaitable, Callable

from s2python.s2_parser import UnparsedS2Message


class S2MediumException(Exception):
    ...

class MediumClosedConnectionError(S2MediumException):
    ...

class MediumCouldNotConnectError(S2MediumException):
    ...


class S2MediumConnection(abc.ABC):
    @abc.abstractmethod
    async def is_connected(self) -> bool:
        ...

    @abc.abstractmethod
    async def messages(self) -> AsyncGenerator[UnparsedS2Message, None]:
        ...

    @abc.abstractmethod
    async def send(self, message: str) -> None:
        ...


# BuildS2ConnectionAsync = Callable[[S2MediumConnectionAsync], Awaitable["S2AsyncConnection"]]
#
#
# class S2MediumConnectorAsync(abc.ABC):
#     """S2 medium specific factory for S2Connections."""
#
#     @abc.abstractmethod
#     async def set_connection_builder(self,
#                                      builder: BuildS2ConnectionAsync) -> None:
#         ...
#
#     @abc.abstractmethod
#     async def run(self) -> None:
#         """Start up the connection or start listening for new connections.
#
#         This function may block or not depending in the implementation.
#         E.g. it will block if a listening socket is opened, or it may return once a single client
#         connection is established.
#         """
#         ...
#
#     @abc.abstractmethod
#     async def close(self) -> None:
#         """Close the medium connector.
#
#         This does not close any functions created by the connector, only the connector itself.
#         Also, this function may not be implemented in all cases. For instance, if the connector
#         only creates a single client connection and then exits, there is no need to close anything
#         so in those cases this function may be a no-op.
#         """
#         ...
