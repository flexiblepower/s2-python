import asyncio
import logging
import uuid
from typing import Any, Coroutine, Optional, Type, Dict, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from s2python.connection.async_.connection import S2AsyncConnection

from s2python.common import ReceptionStatusValues
from s2python.connection.types import S2ConnectionEvent, S2ConnectionEventsAndMessages
from s2python.message import S2Message, S2MessageWithID


logger = logging.getLogger("s2python")

S2EventHandlerAsync = Callable[["S2AsyncConnection", S2ConnectionEvent, Optional[Coroutine[Any, Any, None]]], Coroutine[Any, Any, None]]

class SendOkay:
    _status_is_send: asyncio.Event
    _connection: "S2AsyncConnection"
    _subject_message_id: uuid.UUID

    def __init__(self, connection: "S2AsyncConnection", subject_message_id: uuid.UUID):
        self._status_is_send = asyncio.Event()
        self._connection = connection
        self._subject_message_id = subject_message_id

    async def run(self) -> None:
        """Send the ReceptionStatus OK asynchronously and register it."""
        self._status_is_send.set()

        await self._connection.respond_with_reception_status(  # pylint: disable=protected-access
            subject_message_id=self._subject_message_id,
            status=ReceptionStatusValues.OK,
            diagnostic_label="Processed okay.",
        )

    async def ensure_send(self, type_msg: Type[S2Message]) -> None:
        """Ensure that the ReceptionStatus has been send.

        Send the ReceptionStatus OK if it hasn't been send yet.

        :param type_msg: The type of S2 message for which the ReceptionStatus should have been send. Logging purposes.
        """
        if not self._status_is_send.is_set():
            logger.warning(
                "Handler for message %s %s did not call send_okay / function to send the ReceptionStatus. "
                "Sending it now.",
                type_msg,
                self._subject_message_id,
            )
            await self.run()


class MessageHandlers:
    handlers: Dict[Type[S2ConnectionEventsAndMessages], S2EventHandlerAsync]

    def __init__(self) -> None:
        self.handlers = {}

    async def handle_event(self, connection: "S2AsyncConnection", event: S2ConnectionEventsAndMessages) -> None:
        """Handle the S2 message using the registered handler.

        :param connection: The S2 conncetion the `msg` is received from.
        :param msg: The S2 message
        """
        handler = self.handlers.get(type(event))
        if handler is not None:
            send_okay = None
            try:
                if hasattr(event, "message_id"):
                    logger.debug('Handling S2 message with message id %s using handler %s', event.message_id, handler)
                    send_okay = SendOkay(connection, event.message_id)
                    await handler(connection, event, send_okay.run())
                else:
                    logger.debug('Handling S2 connection event (without message id) using handler %s', handler)
                    await handler(connection, event, None)
            except Exception:
                if send_okay and not send_okay._status_is_send.is_set():
                    await connection.respond_with_reception_status(
                        subject_message_id=event.message_id,
                        status=ReceptionStatusValues.PERMANENT_ERROR,
                        diagnostic_label=f"While processing message {event.message_id} "
                                         f"an unrecoverable error occurred.",
                    )
                raise
            if send_okay:
                await send_okay.ensure_send(type(event))
        else:
            logger.warning(
                "Received an event of type %s but no handler is registered. Ignoring the event.",
                type(event),
            )

    def register_handler(
        self, event_type: Type[S2ConnectionEvent], handler: S2EventHandlerAsync
    ) -> None:
        """Register a coroutine function or a normal function as the handler for a specific S2 message type.

        :param msg_type: The S2 message type to attach the handler to.
        :param handler: The function (asynchronuous or normal) which should handle the S2 message.
        """
        self.handlers[event_type] = handler

    def unregister_handler(self, s2_message_type: Type[S2ConnectionEvent]):
        if s2_message_type in self.handlers:
            del self.handlers[s2_message_type]
