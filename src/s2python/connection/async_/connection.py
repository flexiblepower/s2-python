import asyncio
import json
import logging
import uuid
from typing import Optional, Type

from s2python.connection.connection_events import ConnectionStopped
from s2python.connection.async_.medium.s2_medium import (
    S2MediumConnection,
    MediumClosedConnectionError,
    S2AsyncMediumConnection,
    S2SyncToAsyncMediumConnection,
    S2SyncMediumConnection,
)
from s2python.common import (
    ReceptionStatusValues,
    ReceptionStatus,
)
from s2python.connection.async_.message_handlers import MessageHandlers, S2EventHandlerAsync
from s2python.connection.errors import PermanentConnectionError, CouldNotReceiveStatusReceptionError
from s2python.connection.types import S2ConnectionEventsAndMessages
from s2python.reception_status_awaiter import ReceptionStatusAwaiter
from s2python.s2_parser import S2Parser
from s2python.s2_validation_error import S2ValidationError
from s2python.message import S2Message, S2MessageWithID
from s2python.connection.connection_events import ConnectionStarted

logger = logging.getLogger("s2python")


class S2AsyncConnection:
    _eventloop: asyncio.AbstractEventLoop
    _stop_event: asyncio.Event
    """Stop the S2 connection permanently."""
    _received_messages: asyncio.Queue

    _reception_status_awaiter: ReceptionStatusAwaiter
    _medium: S2AsyncMediumConnection
    _s2_parser: S2Parser
    _handlers: MessageHandlers

    def __init__(
        self,
        medium: S2MediumConnection,
        eventloop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self._eventloop = eventloop if eventloop is not None else asyncio.get_event_loop()
        self._stop_event = asyncio.Event()

        self._reception_status_awaiter = ReceptionStatusAwaiter()
        if isinstance(medium, S2AsyncMediumConnection):
            self._medium = medium
        elif isinstance(medium, S2SyncMediumConnection):
            self._medium = S2SyncToAsyncMediumConnection(medium)
        else:
            raise RuntimeError(
                f"Unexpected medium type {type(medium)}. Medium must be either an "
                "S2AsyncMediumConnection or S2SyncMediumConnection."
            )
        self._s2_parser = S2Parser()
        self._handlers = MessageHandlers()

    async def stop(self) -> None:
        """Stop the S2 connection gracefully.

        Note: Does not stop the underlying medium!
        """
        logger.info("Will stop the S2 connection at the earliest moment.")
        self._stop_event.set()

    async def _wait_till_stop(self) -> None:
        await self._stop_event.wait()

    async def run(self) -> None:
        logger.debug("Starting S2 connection on eventloop %s.", id(self._eventloop))
        self._received_messages = asyncio.Queue()

        if not await self._medium.is_connected():
            raise MediumClosedConnectionError(
                "Cannot start the S2 connection if the underlying medium is closed."
            )

        background_tasks = [
            self._eventloop.create_task(self._receive_messages()),
            self._eventloop.create_task(self._wait_till_stop()),
            self._eventloop.create_task(self._handle_received_messages()),
        ]

        await self._handlers.handle_event(self, ConnectionStarted())

        (done, pending) = await asyncio.wait(background_tasks, return_when=asyncio.FIRST_COMPLETED)

        await self._handlers.handle_event(self, ConnectionStopped())

        for task in pending:
            try:
                task.cancel()
                await task
            except (asyncio.CancelledError, Exception):  # pylint: disable=broad-exception-caught
                pass

        for task in done:
            try:
                await task
            except asyncio.CancelledError:
                pass
            except MediumClosedConnectionError:
                logger.info("The other party closed the websocket connection.")
            except Exception:  # pylint: disable=broad-exception-caught
                logger.exception(
                    "An error occurred in the S2 connection. Terminating current connection."
                )

    async def _handle_received_messages(self) -> None:
        while not self._stop_event.is_set():
            msg = await self._received_messages.get()
            logger.debug("Handling received message %s", msg.to_json())
            await self._handlers.handle_event(self, msg)

    async def _receive_messages(self) -> None:
        """Receives all incoming messages in the form of a generator.

        Will also receive the ReceptionStatus messages but instead of yielding these messages, they are routed
        to any calls of `send_msg_and_await_reception_status`.
        """
        logger.info("S2 connection has started to receive messages.")

        async for message in self._medium.messages():
            try:
                s2_msg: S2Message = self._s2_parser.parse_as_any_message(message)
            except json.JSONDecodeError:
                await self.send_and_forget(
                    ReceptionStatus(
                        subject_message_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                        status=ReceptionStatusValues.INVALID_DATA,
                        diagnostic_label="Not valid json.",
                    )
                )
            except S2ValidationError as e:
                json_msg = json.loads(message)
                message_id = json_msg.get("message_id")
                if message_id:
                    await self.respond_with_reception_status(
                        subject_message_id=message_id,
                        status=ReceptionStatusValues.INVALID_MESSAGE,
                        diagnostic_label=str(e),
                    )
                else:
                    await self.respond_with_reception_status(
                        subject_message_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                        status=ReceptionStatusValues.INVALID_DATA,
                        diagnostic_label="Message appears valid json but could not find a message_id field.",
                    )
            else:
                logger.debug("Received message %s", s2_msg.to_json())

                if isinstance(s2_msg, ReceptionStatus):
                    logger.debug(
                        "Message is a reception status for %s so registering in cache.",
                        s2_msg.subject_message_id,
                    )
                    await self._reception_status_awaiter.receive_reception_status(s2_msg)
                else:
                    logger.debug(
                        "Message is not a reception status, putting it in the received messages queue."
                    )
                    await self._received_messages.put(s2_msg)

    def register_handler(
        self, event_type: Type[S2ConnectionEventsAndMessages], handler: S2EventHandlerAsync
    ) -> None:
        """Register a handler for a specific S2 message type.

        :param event_type: The S2 connection event to register the handler for.
        :param handler: The handler function (asynchronous or normal) which will handle the message.
        """
        self._handlers.register_handler(event_type, handler)

    def unregister_handler(self, s2_message_type: Type[S2ConnectionEventsAndMessages]) -> None:
        self._handlers.unregister_handler(s2_message_type)

    async def send_and_forget(self, s2_msg: S2Message) -> None:
        json_msg = s2_msg.to_json()
        logger.debug("Sending message %s", json_msg)
        try:
            await self._medium.send(json_msg)
        except MediumClosedConnectionError as e:
            logger.error("Unable to send message %s due to %s", s2_msg, str(e))
            raise

    async def respond_with_reception_status(
        self, subject_message_id: uuid.UUID, status: ReceptionStatusValues, diagnostic_label: str
    ) -> None:
        logger.debug("Responding to message %s with status %s", subject_message_id, status)
        await self.send_and_forget(
            ReceptionStatus(
                subject_message_id=subject_message_id,
                status=status,
                diagnostic_label=diagnostic_label,
            )
        )

    async def send_msg_and_await_reception_status(
        self,
        s2_msg: S2MessageWithID,
        timeout_reception_status: float = 5.0,
        raise_on_error: bool = True,
    ) -> ReceptionStatus:
        """Send an S2 message and wait for the corresponding ReceptionStatus message.

        :param s2_msg: The S2 message to send.
        :param timeout_reception_status: How long to wait for the ReceptionStatus message before giving up and raising
        a TimeoutError. Note that if the connection is stopped while waiting, a CouldNotReceiveStatusReceptionError
        will be raised instead.
        :param raise_on_error: Throw an error in case the ReceptionStatus message has a status other than OK. If set to
        False, the ReceptionStatus will be returned even if it contains an error status.
        :raises TimeoutError: If no ReceptionStatus message is received within the specified timeout.
        :raises CouldNotReceiveStatusReceptionError: If the connection is stopped while waiting for the ReceptionStatus message.
        :raises PermanentConnectionError: If a ReceptionStatus message with status PERMANENT_ERROR is received and raise_on_error is True.
        :raises RuntimeError: If a ReceptionStatus message with a status other than OK or PERMANENT_ERROR is received and raise_on_error is True.
        :return: The ReceptionStatus associated with this S2 message.
        """
        await self.send_and_forget(s2_msg)
        logger.debug(
            "Waiting for ReceptionStatus for %s %s seconds",
            s2_msg.message_id,
            timeout_reception_status,
        )
        reception_status_task = self._eventloop.create_task(
            self._reception_status_awaiter.wait_for_reception_status(
                s2_msg.message_id, timeout_reception_status
            )
        )
        stop_event_task = self._eventloop.create_task(self._wait_till_stop())

        (done, pending) = await asyncio.wait(
            [reception_status_task, stop_event_task], return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            try:
                task.cancel()
                await task
            except (asyncio.CancelledError, Exception):  # pylint: disable=broad-exception-caught
                pass

        if reception_status_task in done:
            try:
                reception_status = await reception_status_task
            except (TimeoutError, asyncio.TimeoutError):
                logger.error("Did not receive a reception status on time for %s", s2_msg.message_id)
                self._stop_event.set()
                raise
        else:
            # stop_event_task in done
            await stop_event_task
            raise CouldNotReceiveStatusReceptionError(
                f"Connection stopped while waiting for ReceptionStatus for message {s2_msg.message_id}"
            )

        if raise_on_error:
            if reception_status.status == ReceptionStatusValues.PERMANENT_ERROR:
                error = f"Received a permanent error for message {s2_msg.message_id} with diagnostic label: {reception_status.diagnostic_label}"
                logger.error(error)
                raise PermanentConnectionError(error)
            if reception_status.status != ReceptionStatusValues.OK and raise_on_error:
                raise RuntimeError(
                    f"ReceptionStatus was not OK but rather {reception_status.status}"
                )

        return reception_status
