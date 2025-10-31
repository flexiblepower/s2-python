import abc
import typing

from s2python.common import ControlType as ProtocolControlType
from s2python.frbc import FRBCInstruction
from s2python.ppbc import PPBCScheduleInstruction
from s2python.ombc import OMBCInstruction
from s2python.message import S2Message

if typing.TYPE_CHECKING:
    from s2python.s2_connection import S2Connection, MessageHandlers


