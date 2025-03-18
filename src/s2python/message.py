from typing import Union

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
from s2python.ppbc import (
    PPBCScheduleInstruction,
)

from s2python.common import (
    Duration,
    Handshake,
    HandshakeResponse,
    InstructionStatusUpdate,
    NumberRange,
    PowerForecast,
    PowerForecastElement,
    PowerForecastValue,
    PowerMeasurement,
    PowerRange,
    PowerValue,
    ReceptionStatus,
    ResourceManagerDetails,
    RevokeObject,
    Role,
    SelectControlType,
    SessionRequest,
    Timer,
    Transition,
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
    Duration,
    Handshake,
    HandshakeResponse,
    InstructionStatusUpdate,
    NumberRange,
    PowerForecast,
    PowerForecastElement,
    PowerForecastValue,
    PowerMeasurement,
    PowerRange,
    PowerValue,
    ReceptionStatus,
    ResourceManagerDetails,
    RevokeObject,
    Role,
    SelectControlType,
    SessionRequest,
    Timer,
    Transition,
]
