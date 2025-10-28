from s2python.connection.medium.s2_medium import S2Medium, MediumClosedConnectionError

import asyncio
import json
import logging
import time
import threading
import uuid
from dataclasses import dataclass
from typing import Any, Coroutine, Optional, List, Type, Dict, Callable, Awaitable, Union



from s2python.common import (
    ReceptionStatusValues,
    ReceptionStatus,
    Handshake,
    EnergyManagementRole,
    Role,
    HandshakeResponse,
    ResourceManagerDetails,
    Duration,
    Currency,
    SelectControlType,
)
from s2python.generated.gen_s2 import CommodityQuantity
from s2python.reception_status_awaiter import ReceptionStatusAwaiter
from s2python.s2_control_type import S2ControlType
from s2python.s2_parser import S2Parser
from s2python.s2_validation_error import S2ValidationError
from s2python.message import S2Message, S2MessageWithID
from s2python.version import S2_VERSION

logger = logging.getLogger("s2python")



class CouldNotReceiveStatusReceptionError(Exception):
    ...

@dataclass
class AssetDetails:  # pylint: disable=too-many-instance-attributes
    resource_id: uuid.UUID

    provides_forecast: bool
    provides_power_measurements: List[CommodityQuantity]

    instruction_processing_delay: Duration
    roles: List[Role]
    currency: Optional[Currency] = None

    name: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    serial_number: Optional[str] = None

    def to_resource_manager_details(
        self, control_types: List[S2ControlType]
    ) -> ResourceManagerDetails:
        return ResourceManagerDetails(
            available_control_types=[
                control_type.get_protocol_control_type()
                for control_type in control_types
            ],
            currency=self.currency,
            firmware_version=self.firmware_version,
            instruction_processing_delay=self.instruction_processing_delay,
            manufacturer=self.manufacturer,
            message_id=uuid.uuid4(),
            model=self.model,
            name=self.name,
            provides_forecast=self.provides_forecast,
            provides_power_measurement_types=self.provides_power_measurements,
            resource_id=self.resource_id,
            roles=self.roles,
            serial_number=self.serial_number,
        )


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


class S2AsyncRM:
    connection: 'S2AsyncConnection'

    def __init__(self):
        self.connection._handlers.register_handler(
            SelectControlType, self._handle_select_control_type
        )
        self.connection._handlers.register_handler(Handshake, self._handle_handshake)
        self.connection._handlers.register_handler(HandshakeResponse, self._handle_handshake_response)

    async def _connect_as_rm(self) -> None:
        await self.connection.send_msg_and_await_reception_status(
            Handshake(
                message_id=uuid.uuid4(),
                role=self.role,
                supported_protocol_versions=[S2_VERSION],
            )
        )
        logger.debug(
            "Send handshake to CEM. Expecting Handshake and HandshakeResponse from CEM."
        )

    async def _handle_handshake(
        self, connection: "S2AsyncConnection", message: S2Message, send_okay: Awaitable[None]
    ) -> None:
        if not isinstance(message, Handshake):
            logger.error(
                "Handler for Handshake received a message of the wrong type: %s",
                type(message),
            )
            return

        logger.debug(
            "%s supports S2 protocol versions: %s",
            message.role,
            message.supported_protocol_versions,
        )
        await send_okay

    async def _handle_handshake_response(
        self, connection: "S2AsyncConnection", message: S2Message, send_okay: Awaitable[None]
    ) -> None:
        if not isinstance(message, HandshakeResponse):
            logger.error(
                "Handler for HandshakeResponse received a message of the wrong type: %s",
                type(message),
            )
            return

        logger.debug("Received HandshakeResponse %s", message.to_json())

        logger.debug(
            "CEM selected to use version %s", message.selected_protocol_version
        )
        await send_okay
        logger.debug("Handshake complete. Sending first ResourceManagerDetails.")

        await connection.send_msg_and_await_reception_status(
            self.asset_details.to_resource_manager_details(self.control_types)
        )

    async def _handle_select_control_type(
        self, connection: "S2AsyncConnection", message: S2Message, send_okay: Awaitable[None]
    ) -> None:
        if not isinstance(message, SelectControlType):
            logger.error(
                "Handler for SelectControlType received a message of the wrong type: %s",
                type(message),
            )
            return

        await send_okay

        logger.debug(
            "CEM selected control type %s. Activating control type.",
            message.control_type,
        )

        control_types_by_protocol_name = {
            c.get_protocol_control_type(): c for c in self.control_types
        }
        selected_control_type: Optional[S2ControlType] = (
            control_types_by_protocol_name.get(message.control_type)
        )

        if self._current_control_type is not None:
            await self._eventloop.run_in_executor(
                None, self._current_control_type.deactivate, self
            )

        self._current_control_type = selected_control_type

        if self._current_control_type is not None:
            await self._eventloop.run_in_executor(
                None, self._current_control_type.activate, self
            )
            self._current_control_type.register_handlers(self._handlers)


class S2AsyncConnection:  # pylint: disable=too-many-instance-attributes
    url: str
    reconnect: bool
    reception_status_awaiter: ReceptionStatusAwaiter
    medium: S2Medium
    s2_parser: S2Parser
    control_types: List[S2ControlType]
    role: EnergyManagementRole
    asset_details: AssetDetails

    _handlers: MessageHandlers
    _current_control_type: Optional[S2ControlType]
    _received_messages: asyncio.Queue

    _eventloop: asyncio.AbstractEventLoop
    _main_task: Optional[asyncio.Task]
    _stop_event: asyncio.Event
    """Stop the S2 connection permanently."""
    _restart_connection_event: asyncio.Event
    """Stop the S2 connection but restart if configured."""
    _verify_certificate: bool
    _bearer_token: Optional[str]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        url: str,
        role: EnergyManagementRole,
        control_types: List[S2ControlType],
        asset_details: AssetDetails,
        medium: S2Medium,
        reconnect: bool = False,
        verify_certificate: bool = True,
        bearer_token: Optional[str] = None,
        eventloop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self.url = url
        self.reconnect = reconnect
        self.reception_status_awaiter = ReceptionStatusAwaiter()
        self.medium = medium
        self.s2_parser = S2Parser()

        self._handlers = MessageHandlers()
        self._current_control_type = None

        self._eventloop = eventloop if eventloop is not None else asyncio.get_event_loop()

        self.control_types = control_types
        self.role = role
        self.asset_details = asset_details
        self._verify_certificate = verify_certificate

        self._main_task = None
        self._bearer_token = bearer_token

    async def start_as_rm(self) -> None:
        """Start this connection as a S2 resource manager and connect to a S2 CEM.

        This method will return until the connection is stopped.
        """
        logger.debug('Starting S2 connection as RM.')

        self._main_task = self._eventloop.create_task(self._run_as(self._connect_as_rm()))

    async def stop(self) -> None:
        """Stop the S2 connection gracefully and wait till it stops.

        Note: Not thread-safe. Must be run from the same event loop as `start_as_rm` runs in.
        """
        logger.info("Will stop the S2 connection.")
        self._stop_event.set()
        if self._main_task is not None:
            await self._main_task

    async def _run_as(self, role_task: Coroutine[None, None, None]) -> None:
        logger.debug("Connecting as S2 resource manager.")

        self._stop_event = asyncio.Event()

        first_run = True

        while (first_run or self.reconnect) and not self._stop_event.is_set():
            if not first_run:
                time.sleep(1)
            first_run = False
            self._restart_connection_event = asyncio.Event()
            await self._connect_and_run(role_task)

        logger.debug("Finished S2 connection.")

    async def _wait_till_stop(self) -> None:
        await self._stop_event.wait()

    async def _wait_till_connection_restart(self) -> None:
        await self._restart_connection_event.wait()

    async def _connect_and_run(self, role_task: Coroutine[None, None, None]) -> None:
        self._received_messages = asyncio.Queue()
        await self.medium.connect()
        if self.medium.is_connected():
            background_tasks = [
                self._eventloop.create_task(self._receive_messages()),
                self._eventloop.create_task(self._wait_till_stop()),
                self._eventloop.create_task(self._handle_received_messages()),
                self._eventloop.create_task(self._wait_till_connection_restart()),
            ]

            (done, pending) = await asyncio.wait(
                background_tasks, return_when=asyncio.FIRST_COMPLETED
            )
            if self._current_control_type:
                self._current_control_type.deactivate(self)
                self._current_control_type = None

            for task in done:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                except MediumClosedConnectionError:
                    logger.info("The other party closed the websocket connection.")
                except Exception:
                    logger.exception("An error occurred in the S2 connection. Terminating current connection.")

            for task in pending:
                try:
                    task.cancel()
                    await task
                except (asyncio.CancelledError, Exception):
                    pass

            await self.medium.close()

    async def _handle_received_messages(self) -> None:
        while True:
            msg = await self._received_messages.get()
            await self._handlers.handle_message(self, msg)

    async def _receive_messages(self) -> None:
        """Receives all incoming messages in the form of a generator.

        Will also receive the ReceptionStatus messages but instead of yielding these messages, they are routed
        to any calls of `send_msg_and_await_reception_status`.
        """
        if self.medium is None:
            raise RuntimeError(
                "Cannot receive messages if websocket connection is not yet established."
            )

        logger.info("S2 connection has started to receive messages.")

        async for message in await self.medium.messages():
            try:
                s2_msg: S2Message = self.s2_parser.parse_as_any_message(message)
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
                    await self.reception_status_awaiter.receive_reception_status(s2_msg)
                else:
                    await self._received_messages.put(s2_msg)

    async def send_and_forget(self, s2_msg: S2Message) -> None:
        if self.medium is None:
            raise RuntimeError(
                "Cannot send messages if the S2 medium is not yet established."
            )

        json_msg = s2_msg.to_json()
        logger.debug("Sending message %s", json_msg)
        try:
            await self.medium.send(json_msg)
        except MediumClosedConnectionError as e:
            logger.error("Unable to send message %s due to %s", s2_msg, str(e))
            self._restart_connection_event.set()

    async def respond_with_reception_status(
        self, subject_message_id: uuid.UUID, status: ReceptionStatusValues, diagnostic_label: str
    ) -> None:
        logger.debug(
            "Responding to message %s with status %s", subject_message_id, status
        )
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
        await self.send_and_forget(s2_msg)
        logger.debug(
            "Waiting for ReceptionStatus for %s %s seconds",
            s2_msg.message_id,
            timeout_reception_status,
        )
        try:
            reception_status_task = self._eventloop.create_task(self.reception_status_awaiter.wait_for_reception_status(
                s2_msg.message_id, timeout_reception_status
            ))
            restart_event_task = self._eventloop.create_task(self._restart_connection_event.wait())

            (done, pending) = await asyncio.wait([reception_status_task, restart_event_task], return_when=asyncio.FIRST_COMPLETED)

            if reception_status_task in done:
                reception_status = await reception_status_task
            else:
                raise CouldNotReceiveStatusReceptionError(f"Connection restarted while waiting for ReceptionStatus for message {s2_msg.message_id}")
            #TODO Still need to cancel pending tasks?
        except TimeoutError:
            logger.error("Did not receive a reception status on time for %s",s2_msg.message_id)
            self._restart_connection_event.set()
            raise

        if reception_status.status != ReceptionStatusValues.OK and raise_on_error:
            raise RuntimeError(f"ReceptionStatus was not OK but rather {reception_status.status}")

        return reception_status
