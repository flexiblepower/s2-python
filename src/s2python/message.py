from typing import Union
from pydantic import BaseModel

from s2python.frbc import (
    FRBCActuatorStatus,
    FRBCFillLevelTargetProfile,
    FRBCInstruction,
    FRBCLeakageBehaviour,
    FRBCStorageStatus,
    FRBCSystemDescription,
    FRBCTimerStatus,
    FRBCUsageForecast
)

from s2python.common import (
    Handshake,
    HandshakeResponse,
    InstructionStatusUpdate,
    PowerForecast,
    PowerMeasurement,
    ReceptionStatus,
    ResourceManagerDetails,
    RevokeObject,
    SelectControlType,
    SessionRequest
)

S2Message = Union[
    FRBCActuatorStatus,
    FRBCFillLevelTargetProfile,
    FRBCInstruction,
    FRBCLeakageBehaviour,
    FRBCStorageStatus,
    FRBCSystemDescription,
    FRBCTimerStatus,
    FRBCUsageForecast,
    Handshake,
    HandshakeResponse,
    InstructionStatusUpdate,
    PowerForecast,
    PowerMeasurement,
    ReceptionStatus,
    ResourceManagerDetails,
    RevokeObject,
    SelectControlType,
    SessionRequest,
]