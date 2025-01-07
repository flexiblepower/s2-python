import uuid

from s2python.generated.gen_s2 import DDBCInstruction as GenDDBCInstruction
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class DDBCInstruction(GenDDBCInstruction, S2Message["DDBCInstruction"]):
    model_config = GenDDBCInstruction.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenDDBCInstruction.model_fields["message_id"]  # type: ignore[assignment]
    actuator_id: uuid.UUID = GenDDBCInstruction.model_fields["actuator_id"]  # type: ignore[assignment]
    operation_mode_id: uuid.UUID = GenDDBCInstruction.model_fields["operation_mode_id"]  # type: ignore[assignment]
    operation_mode_factor: float = GenDDBCInstruction.model_fields["operation_mode_factor"]  # type: ignore[assignment]
    abnormal_condition: bool = GenDDBCInstruction.model_fields["abnormal_condition"]  # type: ignore[assignment]
