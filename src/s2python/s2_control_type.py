import abc
import typing

from s2python.common import ControlType as ProtocolControlType
from s2python.frbc import FRBCInstruction

if typing.TYPE_CHECKING:
    from s2python.s2_connection import S2Connection, MessageHandlers


class S2ControlType(abc.ABC):
    @abc.abstractmethod
    def get_protocol_control_type(self) -> ProtocolControlType: ...

    @abc.abstractmethod
    def register_handlers(self, handlers: MessageHandlers) -> None: ...

    @abc.abstractmethod
    def activate(self) -> None: ...

    @abc.abstractmethod
    def deactivate(self) -> None: ...


class FRBCControlType(S2ControlType):
    def get_protocol_control_type(self) -> ProtocolControlType:
        return ProtocolControlType.FILL_RATE_BASED_CONTROL

    def register_handlers(self, handlers: MessageHandlers) -> None:
        handlers.register_handler(FRBCInstruction, self.handle_instruction)

    @abc.abstractmethod
    def handle_instruction(self, conn: S2Connection, msg: FRBCInstruction) -> None: ...

    @abc.abstractmethod
    def activate(self) -> None: ...

    @abc.abstractmethod
    def deactivate(self) -> None: ...


class NoControlControlType(S2ControlType):
    def get_protocol_control_type(self) -> ProtocolControlType:
        return ProtocolControlType.NOT_CONTROLABLE

    def register_handlers(self, handlers: MessageHandlers) -> None:
        pass

    @abc.abstractmethod
    def activate(self) -> None: ...

    @abc.abstractmethod
    def deactivate(self) -> None: ...
