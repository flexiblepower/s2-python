from typing import Union

from s2python.frbc import (
    FRBCActuatorDescription,
    FRBCActuatorStatus,
    FRBCFillLevelTargetProfile,
    FRBCFillLevelTargetProfileElement,
    FRBCInstruction,
    FRBCLeakageBehaviour,
    FRBCLeakageBehaviourElement,
    FRBCOperationMode,
    FRBCOperationModeElement,
    FRBCStorageDescription,
    FRBCStorageStatus,
    FRBCSystemDescription,
    FRBCTimerStatus,
    FRBCUsageForecast,
    FRBCUsageForecastElement,
)
from s2python.ppbc import (
    PPBCEndInterruptionInstruction,
    PPBCPowerProfileDefinition,
    PPBCPowerSequenceContainer,
    PPBCPowerSequence,
    PPBCPowerProfileStatus,
    PPBCPowerSequenceContainerStatus,
    PPBCPowerSequenceElement,
    PPBCScheduleInstruction,
    PPBCStartInterruptionInstruction,
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
    FRBCInstruction,
    FRBCStorageDescription,
    FRBCStorageStatus,
    FRBCSystemDescription,
    FRBCTimerStatus,
    FRBCUsageForecast,
    PPBCScheduleInstruction,
    PPBCStartInterruptionInstruction,
    ReceptionStatus,
    ResourceManagerDetails,
    RevokeObject,
    SelectControlType,
    SessionRequest,
]

S2MessageElement = Union[
    FRBCActuatorDescription,
    FRBCFillLevelTargetProfile,
    FRBCFillLevelTargetProfileElement,
    FRBCLeakageBehaviour,
    FRBCLeakageBehaviourElement,
    FRBCOperationMode,
    FRBCOperationModeElement,
    FRBCUsageForecastElement,
    PPBCEndInterruptionInstruction,
    PPBCPowerProfileDefinition,
    PPBCPowerSequenceContainer,
    PPBCPowerSequence,
    PPBCPowerProfileStatus,
    PPBCPowerSequenceContainerStatus,
    PPBCPowerSequenceElement,
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
    Role,
    Timer,
    Transition,
]
