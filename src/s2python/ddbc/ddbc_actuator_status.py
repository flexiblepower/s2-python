import uuid

from s2python.generated.gen_s2 import DDBCActuatorStatus as GenDDBCActuatorStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class DDBCActuatorStatus(GenDDBCActuatorStatus, S2Message["DDBCActuatorStatus"]):
    model_config = GenDDBCActuatorStatus.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenDDBCActuatorStatus.model_fields["message_id"]  # type: ignore[assignment]
    actuator_id: uuid.UUID = GenDDBCActuatorStatus.model_fields["actuator_id"]  # type: ignore[assignment]
    active_operation_mode_id: uuid.UUID = GenDDBCActuatorStatus.model_fields[
        "active_operation_mode_id"
    ]  # type: ignore[assignment]
    operation_mode_factor: float = GenDDBCActuatorStatus.model_fields[
        "operation_mode_factor"
    ]  # type: ignore[assignment]
