import asyncio
import logging
import threading
import uuid
from typing import Type, Dict, Callable, Awaitable, Union, TYPE_CHECKING

from s2python.common import ReceptionStatusValues
from s2python.message import S2Message

if TYPE_CHECKING:
    from s2python.s2_connection import S2Connection

logger = logging.getLogger("s2python")


S2MessageHandler = Union[
    Callable[["S2Connection", S2Message, Callable[[], None]], None],
    Callable[["S2Connection", S2Message, Awaitable[None]], Awaitable[None]],
]


class SendOkay:
    status_is_send: threading.Event
    connection: "S2Connection"
    subject_message_id: uuid.UUID

    def __init__(self, connection: "S2Connection", subject_message_id: uuid.UUID):
        self.status_is_send = threading.Event()
        self.connection = connection
        self.subject_message_id = subject_message_id

    async def run_async(self) -> None:
        self.status_is_send.set()

        await self.connection._respond_with_reception_status(  # pylint: disable=protected-access
            subject_message_id=self.subject_message_id,
            status=ReceptionStatusValues.OK,
            diagnostic_label="Processed okay.",
        )

    def run_sync(self) -> None:
        self.status_is_send.set()

        self.connection.respond_with_reception_status_sync(
            subject_message_id=self.subject_message_id,
            status=ReceptionStatusValues.OK,
            diagnostic_label="Processed okay.",
        )

    async def ensure_send_async(self, type_msg: Type[S2Message]) -> None:
        if not self.status_is_send.is_set():
            logger.warning(
                "Handler for message %s %s did not call send_okay / function to send the ReceptionStatus. "
                "Sending it now.",
                type_msg,
                self.subject_message_id,
            )
            await self.run_async()

    def ensure_send_sync(self, type_msg: Type[S2Message]) -> None:
        if not self.status_is_send.is_set():
            logger.warning(
                "Handler for message %s %s did not call send_okay / function to send the ReceptionStatus. "
                "Sending it now.",
                type_msg,
                self.subject_message_id,
            )
            self.run_sync()


class MessageHandlers:
    handlers: Dict[Type[S2Message], S2MessageHandler]

    def __init__(self) -> None:
        self.handlers = {}

    async def handle_message(self, connection: "S2Connection", msg: S2Message) -> None:
        """Handle the S2 message using the registered handler.

        :param connection: The S2 conncetion the `msg` is received from.
        :param msg: The S2 message
        """
        handler = self.handlers.get(type(msg))
        if handler is not None:
            send_okay = SendOkay(connection, msg.message_id)  # type: ignore[attr-defined, union-attr]

            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(connection, msg, send_okay.run_async())  # type: ignore[arg-type]
                    await send_okay.ensure_send_async(type(msg))
                else:

                    def do_message() -> None:
                        handler(connection, msg, send_okay.run_sync)  # type: ignore[arg-type]
                        send_okay.ensure_send_sync(type(msg))

                    eventloop = asyncio.get_event_loop()
                    await eventloop.run_in_executor(executor=None, func=do_message)
            except Exception:
                if not send_okay.status_is_send.is_set():
                    await connection._respond_with_reception_status(  # pylint: disable=protected-access
                        subject_message_id=msg.message_id,  # type: ignore[attr-defined, union-attr]
                        status=ReceptionStatusValues.PERMANENT_ERROR,
                        diagnostic_label=f"While processing message {msg.message_id} "  # type: ignore[attr-defined, union-attr]  # pylint: disable=line-too-long
                        f"an unrecoverable error occurred.",
                    )
                raise
        else:
            logger.warning(
                "Received a message of type %s but no handler is registered. Ignoring the message.",
                type(msg),
            )

    def register_handler(
        self, msg_type: Type[S2Message], handler: S2MessageHandler
    ) -> None:
        """Register a coroutine function or a normal function as the handler for a specific S2 message type.

        :param msg_type: The S2 message type to attach the handler to.
        :param handler: The function (asynchronuous or normal) which should handle the S2 message.
        """
        self.handlers[msg_type] = handler
