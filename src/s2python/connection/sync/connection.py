import asyncio
import logging
import threading
import uuid
from typing import Any, Coroutine, Optional, List, Type, Callable

from s2python.common import (
    ReceptionStatusValues,
    EnergyManagementRole,
)
from s2python.connection.asset_details import AssetDetails
from s2python.connection.types import S2MessageHandlerSync, S2ConnectionEvent
from s2python.s2_control_type import S2ControlType
from s2python.message import S2Message

from s2python.common import ReceptionStatus
from s2python.connection.medium.s2_medium import S2MediumConnectionAsync
from s2python.connection.s2_async_connection import S2AsyncConnection
from s2python.message import S2MessageWithID

logger = logging.getLogger("s2python")

S2EventHandlerSync = Callable[["S2SyncConnection", S2ConnectionEvent, Optional[Callable[[], None]]], None]



class S2SyncConnection:
    _thread: threading.Thread
    _eventloop: asyncio.AbstractEventLoop
    _async_s2_connection: S2AsyncConnection

    def __init__(  # pylint: disable=too-many-arguments
        self,
        role: EnergyManagementRole,
        control_types: List[S2ControlType],
        asset_details: AssetDetails,
        medium: S2MediumConnectionAsync,
        eventloop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self._thread = threading.Thread(target=self._run_eventloop)
        self._eventloop = asyncio.new_event_loop() if eventloop is None else eventloop
        self._async_s2_connection = S2AsyncConnection(role, control_types, asset_details, medium, self._eventloop)

    def start_as_rm(self) -> None:
        self._thread.start()
        asyncio.run_coroutine_threadsafe(
            self._async_s2_connection.start_as_rm(),
            self._eventloop,
        ).result()

    def _run_eventloop(self) -> None:
        logger.debug("Starting synchronous S2 connection event loop in thread %s", self._thread.name)
        self._eventloop.run_forever()
        logger.debug("Synchronous S2 connection event loop in thread %s has stopped", self._thread.name)

    def stop(self) -> None:
        """Stops the S2 connection.

        Note: Ensure this method is called from a different thread than the thread running the S2 connection.
        Otherwise it will block waiting on the coroutine _do_stop to terminate successfully but it can't run
        the coroutine. A `RuntimeError` will be raised to prevent the indefinite block.
        """
        if threading.current_thread() == self._thread:
            raise RuntimeError(
                "Do not call stop from the thread running the S2 connection. This results in an infinite block!"
            )
        if self._eventloop.is_running():
            asyncio.run_coroutine_threadsafe(self._async_s2_connection.stop(), self._eventloop).result()
        self._eventloop.stop()
        self._thread.join()
        logger.info("Stopped the S2 connection.")

    def register_handler(self, s2_message_type: Type[S2MessageWithID], handler: S2MessageHandlerSync) -> None:
        """Register a handler for a specific S2 message type.

        :param s2_message_type: The S2 message type to register the handler for.
        :param handler: The handler function (asynchronous or normal) which will handle the message.
        """

        async def handle_s2_message_async_wrapper(
            _: S2AsyncConnection,
            s2_msg: S2ConnectionEvent,
            send_okay: Coroutine[Any, Any, None],
        ) -> None:
            await self._eventloop.run_in_executor(
                None,
                handler,
                self,
                s2_msg,
                lambda: asyncio.run_coroutine_threadsafe(send_okay, self._eventloop).result(),
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
