import uuid

from s2python.generated.gen_s2 import DDBCInstruction as GenDDBCInstruction
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class DDBCInstruction(GenDDBCInstruction, S2MessageComponent):
    model_config = copy_config(GenDDBCInstruction.model_config, validate_assignment=True)

    message_id: uuid.UUID = copy_field(GenDDBCInstruction.model_fields["message_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    actuator_id: uuid.UUID = copy_field(GenDDBCInstruction.model_fields["actuator_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    operation_mode_id: uuid.UUID = copy_field(GenDDBCInstruction.model_fields["operation_mode_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    operation_mode_factor: float = copy_field(GenDDBCInstruction.model_fields["operation_mode_factor"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    abnormal_condition: bool = copy_field(GenDDBCInstruction.model_fields["abnormal_condition"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
