import asyncio
import logging
import uuid
from typing import Any, Coroutine, Optional, Type, Callable

from s2python.common import (
    ReceptionStatusValues,
)
from s2python.connection.types import S2ConnectionEvent, S2ConnectionEventsAndMessages
from s2python.message import S2Message

from s2python.common import ReceptionStatus
from s2python.connection.async_.medium.s2_medium import S2MediumConnection
from s2python.connection.async_ import S2AsyncConnection
from s2python.message import S2MessageWithID

logger = logging.getLogger("s2python")

S2EventHandlerSync = Callable[["S2SyncConnection", S2ConnectionEvent, Optional[Callable[[], None]]], None]


class S2SyncConnection:
    _eventloop: asyncio.AbstractEventLoop
    _async_s2_connection: S2AsyncConnection

    def __init__(
        self,
        medium: S2MediumConnection,
        eventloop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self._eventloop = asyncio.new_event_loop() if eventloop is None else eventloop
        self._async_s2_connection = self._eventloop.run_until_complete(S2SyncConnection._create_async_s2_connection(medium, self._eventloop))

    @staticmethod
    async def _create_async_s2_connection(medium: S2MediumConnection, eventloop: asyncio.AbstractEventLoop) -> S2AsyncConnection:
        return S2AsyncConnection(medium, eventloop)

    def run(self) -> None:
        self._eventloop.run_until_complete(self._async_s2_connection.run())

    def stop(self) -> None:
        """Gracefully stops the S2 connection."""
        asyncio.run_coroutine_threadsafe(self._async_s2_connection.stop(), self._eventloop).result()

    def register_handler(self, s2_message_type: Type[S2ConnectionEventsAndMessages], handler: S2EventHandlerSync) -> None:
        """Register a handler for a specific S2 message type.

        :param s2_message_type: The S2 message type to register the handler for.
        :param handler: The handler function (asynchronous or normal) which will handle the message.
        """

        async def handle_s2_message_async_wrapper(
            _: S2AsyncConnection,
            s2_msg: S2ConnectionEvent,
            send_okay: Optional[Callable[[], Coroutine[Any, Any, None]]],
        ) -> None:
            await self._eventloop.run_in_executor(
                None,
                handler,
                self,
                s2_msg,
                lambda: asyncio.run_coroutine_threadsafe(send_okay(), self._eventloop).result() if send_okay else None,
            )

        self._async_s2_connection.register_handler(s2_message_type, handle_s2_message_async_wrapper)

    def unregister_handler(self, s2_message_type: Type[S2MessageWithID]) -> None:
        self._async_s2_connection.unregister_handler(s2_message_type)

    def send_and_forget(
        self, s2_msg: S2Message
    ) -> None:
        asyncio.run_coroutine_threadsafe(
            self._async_s2_connection.send_and_forget(s2_msg),
            self._eventloop,
        ).result()

    def respond_with_reception_status(
        self, subject_message_id: uuid.UUID, status: ReceptionStatusValues, diagnostic_label: str
    ) -> None:
        asyncio.run_coroutine_threadsafe(
            self._async_s2_connection.respond_with_reception_status(
                subject_message_id, status, diagnostic_label
            ),
            self._eventloop,
        ).result()

    def send_msg_and_await_reception_status(
        self,
        s2_msg: S2MessageWithID,
        timeout_reception_status: float = 5.0,
        raise_on_error: bool = True,
    ) -> ReceptionStatus:
        return asyncio.run_coroutine_threadsafe(
            self._async_s2_connection.send_msg_and_await_reception_status(
                s2_msg, timeout_reception_status, raise_on_error
            ),
            self._eventloop,
        ).result()
