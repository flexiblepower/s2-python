import abc
import logging
import uuid
from typing import Coroutine, Optional, List, Any, Callable

from s2python.connection.asset_details import AssetDetails
from s2python.common import (
    Handshake,
    EnergyManagementRole,
    HandshakeResponse,
    SelectControlType,
)
from s2python.connection.async_.connection import S2AsyncConnection
from s2python.connection.types import S2ConnectionEvent
from s2python.version import S2_VERSION

from s2python.connection.connection_events import ConnectionStarted

from s2python.common import ControlType as ProtocolControlType
from s2python.frbc import FRBCInstruction
from s2python.ppbc import PPBCScheduleInstruction
from s2python.ombc import OMBCInstruction
from s2python.message import S2Message

logger = logging.getLogger("s2python")


class S2ControlType(abc.ABC):
    @abc.abstractmethod
    def get_protocol_control_type(self) -> ProtocolControlType: ...

    @abc.abstractmethod
    def register_handlers(self, connection: S2AsyncConnection) -> None: ...

    @abc.abstractmethod
    async def activate(self, connection: S2AsyncConnection) -> None: ...

    @abc.abstractmethod
    async def deactivate(self, connection: S2AsyncConnection) -> None: ...



class ResourceManagerHandler:
    asset_details: AssetDetails
    _current_control_type: Optional[S2ControlType]
    _control_types: List[S2ControlType]

    def __init__(self, control_types: List[S2ControlType],
                 asset_details: AssetDetails) -> None:
        self.asset_details = asset_details
        self._current_control_type = None
        self._control_types = control_types

    def get_s2_role(self) -> EnergyManagementRole:
        return EnergyManagementRole.RM

    def register_handlers(self, connection: S2AsyncConnection) -> None:
        connection.register_handler(ConnectionStarted, self._on_connection_started)
        connection.register_handler(Handshake, self._on_handshake)
        connection.register_handler(HandshakeResponse, self._on_handshake_response)
        connection.register_handler(SelectControlType, self._on_select_control_type)

    async def _on_connection_started(self, connection: S2AsyncConnection, _: S2ConnectionEvent, __: Optional[Coroutine[Any, Any, None]]) -> None:
        await connection.send_msg_and_await_reception_status(
            Handshake(
                message_id=uuid.uuid4(),
                role=self.get_s2_role(),
                supported_protocol_versions=[S2_VERSION],
            )
        )
        logger.debug(
            "Send handshake to CEM. Expecting Handshake and HandshakeResponse from CEM."
        )

    async def _on_handshake(
        self, _: S2AsyncConnection, event: S2ConnectionEvent, send_okay: Optional[Coroutine[Any, Any, None]]
    ) -> None:
        assert send_okay is not None
        if not isinstance(event, Handshake):
            logger.error(
                "Handler for Handshake received a message of the wrong type: %s",
                type(event),
            )
            return

        logger.debug(
            "%s supports S2 protocol versions: %s",
            event.role,
            event.supported_protocol_versions,
        )
        await send_okay

    async def _on_handshake_response(
        self, connection: S2AsyncConnection, event: S2ConnectionEvent, send_okay: Optional[Coroutine[Any, Any, None]]
    ) -> None:
        assert send_okay is not None
        if not isinstance(event, HandshakeResponse):
            logger.error(
                "Handler for HandshakeResponse received a message of the wrong type: %s",
                type(event),
            )
            return

        logger.debug("Received HandshakeResponse %s", event.to_json())
        logger.debug(
            "CEM selected to use version %s", event.selected_protocol_version
        )
        await send_okay
        logger.debug("Handshake complete. Sending first ResourceManagerDetails.")

        await connection.send_msg_and_await_reception_status(
            self.asset_details.to_resource_manager_details(self._control_types)
        )

    async def _on_select_control_type(
        self, connection: S2AsyncConnection, event: S2ConnectionEvent, send_okay: Optional[Coroutine[Any, Any, None]]
    ) -> None:
        assert send_okay is not None
        if not isinstance(event, SelectControlType):
            logger.error(
                "Handler for SelectControlType received a message of the wrong type: %s",
                type(event),
            )
            return

        await send_okay

        logger.debug(
            "CEM selected control type %s. Activating control type.",
            event.control_type,
        )

        control_types_by_protocol_name = {
            c.get_protocol_control_type(): c for c in self._control_types
        }
        selected_control_type = control_types_by_protocol_name.get(event.control_type)

        if self._current_control_type is not None:
            await self._current_control_type.deactivate(connection)

        self._current_control_type = selected_control_type

        if self._current_control_type is not None:
            self._current_control_type.register_handlers(connection)
            await self._current_control_type.activate(connection)

    async def _on_connection_stop(self, connection: S2AsyncConnection, __: S2ConnectionEvent, ___: Optional[Coroutine[Any, Any, None]]):
        if self._current_control_type:
            await self._current_control_type.deactivate(connection)
            self._current_control_type = None


class FRBCControlType(S2ControlType):
    def get_protocol_control_type(self) -> ProtocolControlType:
        return ProtocolControlType.FILL_RATE_BASED_CONTROL

    def register_handlers(self, connection: S2AsyncConnection) -> None:
        connection.register_handler(FRBCInstruction, self.handle_instruction)

    @abc.abstractmethod
    async def handle_instruction(
        self, conn: S2AsyncConnection, msg: S2Message, send_okay: Callable[[], None]
    ) -> None: ...

    @abc.abstractmethod
    async def activate(self, connection: S2AsyncConnection) -> None:
        """Overwrite with the actual dctivation logic of your Resource Manager for this particular control type."""

    @abc.abstractmethod
    async def deactivate(self, connection: S2AsyncConnection) -> None:
        """Overwrite with the actual deactivation logic of your Resource Manager for this particular control type."""


class PPBCControlType(S2ControlType):
    def get_protocol_control_type(self) -> ProtocolControlType:
        return ProtocolControlType.POWER_PROFILE_BASED_CONTROL

    def register_handlers(self, connection: S2AsyncConnection) -> None:
        connection.register_handler(PPBCScheduleInstruction, self.handle_instruction)

    @abc.abstractmethod
    async def handle_instruction(
        self, connection: S2AsyncConnection, msg: S2Message, send_okay: Callable[[], None]
    ) -> None: ...

    @abc.abstractmethod
    async def activate(self, connection: S2AsyncConnection) -> None:
        """Overwrite with the actual dctivation logic of your Resource Manager for this particular control type."""

    @abc.abstractmethod
    async def deactivate(self, connection: S2AsyncConnection) -> None:
        """Overwrite with the actual deactivation logic of your Resource Manager for this particular control type."""


class OMBCControlType(S2ControlType):
    def get_protocol_control_type(self) -> ProtocolControlType:
        return ProtocolControlType.OPERATION_MODE_BASED_CONTROL

    def register_handlers(self, connection: S2AsyncConnection) -> None:
        connection.register_handler(OMBCInstruction, self.handle_instruction)

    @abc.abstractmethod
    async def handle_instruction(
        self, connection: S2AsyncConnection, msg: S2Message, send_okay: Callable[[], None]
    ) -> None: ...

    @abc.abstractmethod
    async def activate(self, connection: S2AsyncConnection) -> None:
        """Overwrite with the actual dctivation logic of your Resource Manager for this particular control type."""

    @abc.abstractmethod
    async def deactivate(self, connection: S2AsyncConnection) -> None:
        """Overwrite with the actual deactivation logic of your Resource Manager for this particular control type."""


class PEBCControlType(S2ControlType):
    def get_protocol_control_type(self) -> ProtocolControlType:
        return ProtocolControlType.POWER_ENVELOPE_BASED_CONTROL

    def register_handlers(self, connection: S2AsyncConnection) -> None:
        pass

    @abc.abstractmethod
    async def activate(self, connection: S2AsyncConnection) -> None: ...

    @abc.abstractmethod
    async def deactivate(self, connection: S2AsyncConnection) -> None: ...


class NoControlControlType(S2ControlType):
    def get_protocol_control_type(self) -> ProtocolControlType:
        return ProtocolControlType.NOT_CONTROLABLE

    def register_handlers(self, connection: S2AsyncConnection) -> None:
        pass

    @abc.abstractmethod
    async def activate(self, connection: S2AsyncConnection) -> None: ...

    @abc.abstractmethod
    async def deactivate(self, connection: S2AsyncConnection) -> None: ...
