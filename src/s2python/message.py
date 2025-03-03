from typing import Union

from s2python.frbc import (
    FRBCActuatorStatus,
    FRBCFillLevelTargetProfile,
    FRBCInstruction,
    FRBCLeakageBehaviour,
    FRBCStorageStatus,
    FRBCSystemDescription,
    FRBCTimerStatus,
    FRBCUsageForecast,
)
from s2python.ppbc import (
    PPBCScheduleInstruction,
)
from s2python.ombc import (
    OMBCInstruction,
    OMBCOperationMode,
    OMBCTimerStatus,
    OMBCStatus,
    OMBCSystemDescription,
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
    SessionRequest,
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
    PPBCScheduleInstruction,
    OMBCInstruction,
    OMBCOperationMode,
    OMBCTimerStatus,
    OMBCStatus,
    OMBCSystemDescription,
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
