import asyncio
import inspect
import logging
import threading
import uuid
from dataclasses import dataclass
from typing import Optional, List, Type, Dict, Callable, Awaitable, Union

from websockets.asyncio.client import ClientConnection as WSConnection, connect as ws_connect

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
from s2python.reception_status_awaiter import ReceptionStatusAwaiter
from s2python.s2_control_type import S2ControlType
from s2python.s2_parser import S2Parser
from s2python.validate_values_mixin import S2Message


logger = logging.getLogger("s2python")


@dataclass
class AssetDetails:
    resource_id: str

    instruction_processing_delay: Duration
    roles: List[Role] = None
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
                control_type.get_protocol_control_type() for control_type in control_types
            ],
            currency=self.currency,
            firmware_version=self.firmware_version,
            instruction_processing_delay=self.instruction_processing_delay,
            manufacturer=self.manufacturer,
            message_id=uuid.uuid4(),
            model=self.model,
            name=self.name,
            provides_forecast=True,  # TODO
            provides_power_measurement_types=[],  # TODO
            resource_id=self.resource_id,
            roles=self.roles,
            serial_number=self.serial_number,
        )


S2MessageHandler = Union[
    Callable[["S2Connection", S2Message], None],
    Callable[["S2Connection", S2Message], Awaitable[None]],
]


class MessageHandlers:
    handlers: Dict[Type[S2Message], S2MessageHandler]

    def __init__(self):
        self.handlers = {}

    async def handle_message(self, connection: "S2Connection", msg: S2Message) -> None:
        """Handle the S2 message using the registered handler.

        :param connection: The S2 conncetion the `msg` is received from.
        :param msg: The S2 message
        """
        handler = self.handlers.get(type(msg))

        if handler:
            if inspect.iscoroutinefunction(handler):
                await handler(connection, msg)
            else:
                handler(connection, msg)
        else:
            logger.warning(
                "Received a message of type %s but no handler is registered. Ignoring the message.",
                type(msg),
            )

    def register_handler(self, msg_type: Type[S2Message], handler: S2MessageHandler) -> None:
        """Register a coroutine function or a normal function as the handler for a specific S2 message type.

        :param msg_type: The S2 message type to attach the handler to.
        :param handler: The function (asynchronuous or normal) which should handle the S2 message.
        """
        self.handlers[msg_type] = handler


class S2Connection:
    url: str
    reception_status_awaiter: ReceptionStatusAwaiter
    ws: Optional[WSConnection]
    s2_parser: S2Parser
    control_types: List[S2ControlType]
    role: EnergyManagementRole
    asset_details: AssetDetails

    _thread: threading.Thread
    _received_messages: asyncio.Queue
    _handlers: MessageHandlers
    _receiver_task: asyncio.Task
    _current_control_type: Optional[S2ControlType]

    def __init__(
        self,
        url: str,
        role: EnergyManagementRole,
        control_types: List[S2ControlType],
        asset_details: AssetDetails,
    ):
        self.url = url
        self.reception_status_awaiter = ReceptionStatusAwaiter()
        self.s2_parser = S2Parser()

        self._received_messages = asyncio.Queue()
        self._handlers = MessageHandlers()
        self._current_control_type = None

        self.control_types = control_types
        self.role = role
        self.asset_details = asset_details

        self._handlers.register_handler(SelectControlType, self.handle_select_control_type)

    def start_as_rm(self) -> None:
        self._thread = threading.Thread(target=self._run_as_rm())
        self._thread.start()

    def _run_as_rm(self):
        eventloop = asyncio.new_event_loop()
        eventloop.run_until_complete(self.connect_as_rm())
        eventloop.run_until_complete(self._handle_received_messages())

    async def connect_as_rm(self) -> None:
        self.ws = await ws_connect(uri=self.url)
        self._receiver_task = asyncio.create_task(self._received_messages)

        await self.send_msg_and_await_reception_status(
            Handshake(message_id=uuid.uuid4(), role=self.role, supported_protocol_versions=[])
        )

        logger.debug("Send handshake to CEM. Waiting for Handshake and HandshakeResponse from CEM.")
        cem_handshake_responses = [self._receive_next_message(), self._receive_next_message()]
        handshake_response = next(
            filter(lambda m: isinstance(m, HandshakeResponse), cem_handshake_responses), None
        )
        cem_handshake = next(
            filter(lambda m: isinstance(m, Handshake), cem_handshake_responses), None
        )

        logger.debug(
            "CEM supports S2 protocol versions: %s. CEM selected to use version %s",
            cem_handshake.supported_protocol_versions,
            handshake_response.selected_protocol_version,
        )
        logger.debug("Handshake complete. Sending first ResourceManagerDetails.")

        await self.send_msg_and_await_reception_status(
            self.asset_details.to_resource_manager_details(self.control_types)
        )

    async def handle_select_control_type(self, _: "S2Connection", message: S2Message) -> None:
        logger.debug("CEM selected control type %s. Activating control type.", message.control_type)

        selected_control_type: S2ControlType = next(
            filter(
                lambda c: c.get_protocol_control_type() == message.control_type, self.control_types
            ),
            None,
        )

        if self._current_control_type is not None:
            self._current_control_type.deactivate()

        self._current_control_type = selected_control_type

        if self._current_control_type is not None:
            self._current_control_type.activate()
            self._current_control_type.register_handlers(self._handlers)

    async def _receive_next_message(self) -> S2Message:
        """Receive next non-ReceptionStatus message.

        :return: The next S2 message which is not a ReceptionStatus.
        """
        return await self._received_messages.get()

    async def _receive_messages(self) -> None:
        """Receives all incoming messages in the form of a generator.

        Will also receive the ReceptionStatus messages but instead of yielding these messages, they are routed
        to any calls of `send_msg_and_await_reception_status`.
        """
        async for message in self.ws:
            s2_msg: S2Message = self.s2_parser.parse_as_any_message(message)

            if isinstance(s2_msg, ReceptionStatus):
                await self.reception_status_awaiter.receive_reception_status(s2_msg)
            else:
                await self._received_messages.put(s2_msg)

    async def _send_and_forget(self, s2_msg: S2Message) -> None:
        await self.ws.send(s2_msg.to_json())

    async def send_msg_and_await_reception_status(
        self, s2_msg: S2Message, timeout_reception_status: float = 5.0, raise_on_error: bool = True
    ) -> S2Message:
        await self._send_and_forget(s2_msg)
        reception_status = await self.reception_status_awaiter.wait_for_reception_status(
            s2_msg.message_id, timeout_reception_status
        )

        if reception_status.status != ReceptionStatusValues.OK and raise_on_error:
            raise RuntimeError(f"ReceptionStatus was not OK but rather {reception_status.status}")

        return reception_status

    async def _handle_received_messages(self) -> None:
        while True:
            msg = await self._received_messages.get()
            await self._handlers.handle_message(self, msg)
