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
from s2python.ddbc import (
    DDBCActuatorDescription,
    DDBCActuatorStatus,
    DDBCAverageDemandRateForecast,
    DDBCAverageDemandRateForecastElement,
    DDBCInstruction,
    DDBCOperationMode,
    DDBCSystemDescription,
    DDBCTimerStatus,
)
from s2python.ombc import (
    OMBCInstruction,
    OMBCOperationMode,
    OMBCTimerStatus,
    OMBCStatus,
    OMBCSystemDescription,
)

from s2python.pebc import (
    PEBCAllowedLimitRange,
    PEBCEnergyConstraint,
    PEBCInstruction,
    PEBCPowerConstraints,
    PEBCPowerEnvelope,
    PEBCPowerEnvelopeElement,
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
    DDBCAverageDemandRateForecast,
    DDBCInstruction,
    DDBCSystemDescription,
    DDBCTimerStatus,
    FRBCActuatorStatus,
    FRBCFillLevelTargetProfile,
    FRBCInstruction,
    FRBCLeakageBehaviour,
    FRBCStorageStatus,
    FRBCSystemDescription,
    FRBCTimerStatus,
    FRBCUsageForecast,
    OMBCSystemDescription,
    OMBCStatus,
    OMBCTimerStatus,
    OMBCInstruction,
    PEBCPowerConstraints,
    PPBCEndInterruptionInstruction,
    PPBCPowerProfileDefinition,
    PPBCPowerProfileStatus,
    PPBCScheduleInstruction,
    PPBCStartInterruptionInstruction,
    ResourceManagerDetails,
    RevokeObject,
    SelectControlType,
    SessionRequest,
    DDBCActuatorStatus,
    PEBCEnergyConstraint,
    PEBCInstruction,
    Handshake,
    HandshakeResponse,
    InstructionStatusUpdate,
    PowerForecast,
    PowerMeasurement,
    ReceptionStatus,
]

S2MessageElement = Union[
    DDBCActuatorDescription,
    DDBCAverageDemandRateForecastElement,
    DDBCOperationMode,
    FRBCActuatorDescription,
    FRBCFillLevelTargetProfileElement,
    FRBCLeakageBehaviourElement,
    FRBCOperationMode,
    FRBCOperationModeElement,
    FRBCStorageDescription,
    FRBCUsageForecastElement,
    OMBCOperationMode,
    PEBCAllowedLimitRange,
    PEBCPowerEnvelope,
    PEBCPowerEnvelopeElement,
    PPBCPowerSequenceContainer,
    PPBCPowerSequence,
    PPBCPowerSequenceContainerStatus,
    PPBCPowerSequenceElement,
    Duration,
    NumberRange,
    PowerForecastElement,
    PowerForecastValue,
    PowerRange,
    PowerValue,
    Role,
    Timer,
    Transition,
]
