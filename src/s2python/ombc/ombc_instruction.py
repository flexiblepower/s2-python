import uuid

from s2python.generated.gen_s2 import OMBCInstruction as GenOMBCInstruction
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class OMBCInstruction(GenOMBCInstruction, S2MessageComponent):
    model_config = copy_config(GenOMBCInstruction.model_config, validate_assignment=True)

    id: uuid.UUID = copy_field(GenOMBCInstruction.model_fields["id"])  # type: ignore[assignment]
    message_id: uuid.UUID = copy_field(GenOMBCInstruction.model_fields["message_id"])  # type: ignore[assignment]
    abnormal_condition: bool = copy_field(GenOMBCInstruction.model_fields["abnormal_condition"])  # type: ignore[assignment]
    operation_mode_factor: float = copy_field(GenOMBCInstruction.model_fields["operation_mode_factor"])  # type: ignore[assignment]
    operation_mode_id: uuid.UUID = copy_field(GenOMBCInstruction.model_fields["operation_mode_id"])  # type: ignore[assignment]
