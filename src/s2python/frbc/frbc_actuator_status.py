from typing import Optional
import uuid

from s2python.generated.gen_s2 import FRBCActuatorStatus as GenFRBCActuatorStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class FRBCActuatorStatus(GenFRBCActuatorStatus, S2MessageComponent):
    model_config = GenFRBCActuatorStatus.model_config
    model_config["validate_assignment"] = True

    active_operation_mode_id: uuid.UUID = GenFRBCActuatorStatus.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "active_operation_mode_id"
    ]  # type: ignore[assignment]
    actuator_id: uuid.UUID = GenFRBCActuatorStatus.model_fields["actuator_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    message_id: uuid.UUID = GenFRBCActuatorStatus.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    previous_operation_mode_id: Optional[uuid.UUID] = GenFRBCActuatorStatus.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "previous_operation_mode_id"
    ]  # type: ignore[assignment]
