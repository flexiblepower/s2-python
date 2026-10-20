import uuid

from s2python.generated.gen_s2 import DDBCActuatorStatus as GenDDBCActuatorStatus
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class DDBCActuatorStatus(GenDDBCActuatorStatus, S2MessageComponent):
    model_config = copy_config(GenDDBCActuatorStatus.model_config, validate_assignment=True)

    message_id: uuid.UUID = copy_field(GenDDBCActuatorStatus.model_fields["message_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    actuator_id: uuid.UUID = copy_field(GenDDBCActuatorStatus.model_fields["actuator_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    active_operation_mode_id: uuid.UUID = copy_field(GenDDBCActuatorStatus.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "active_operation_mode_id"
    ])  # type: ignore[assignment]
    operation_mode_factor: float = copy_field(GenDDBCActuatorStatus.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "operation_mode_factor"
    ])  # type: ignore[assignment]
