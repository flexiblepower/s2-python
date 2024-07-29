from typing import Optional
import uuid

from s2python.generated.gen_s2 import FRBCActuatorStatus as GenFRBCActuatorStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class FRBCActuatorStatus(GenFRBCActuatorStatus, S2Message["FRBCActuatorStatus"]):
    model_config = GenFRBCActuatorStatus.model_config
    model_config["validate_assignment"] = True

    active_operation_mode_id: uuid.UUID = GenFRBCActuatorStatus.model_fields[
        "active_operation_mode_id"
    ]  # type: ignore[assignment]
    actuator_id: uuid.UUID = GenFRBCActuatorStatus.model_fields["actuator_id"]  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCActuatorStatus.model_fields["message_id"]  # type: ignore[assignment]
    previous_operation_mode_id: Optional[uuid.UUID] = GenFRBCActuatorStatus.model_fields[
        "previous_operation_mode_id"
    ]  # type: ignore[assignment]
