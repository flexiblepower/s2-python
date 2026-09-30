import uuid

from s2python.generated.gen_s2 import OMBCStatus as GenOMBCStatus

from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class OMBCStatus(GenOMBCStatus, S2MessageComponent):
    model_config = copy_config(GenOMBCStatus.model_config, validate_assignment=True)

    message_id: uuid.UUID = copy_field(GenOMBCStatus.model_fields["message_id"])  # type: ignore[assignment]
    operation_mode_factor: float = copy_field(GenOMBCStatus.model_fields["operation_mode_factor"])  # type: ignore[assignment]
