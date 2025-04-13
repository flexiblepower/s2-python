import uuid

from s2python.generated.gen_s2 import OMBCStatus as GenOMBCStatus

from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class OMBCStatus(GenOMBCStatus, S2MessageComponent):
    model_config = GenOMBCStatus.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenOMBCStatus.model_fields["message_id"]  # type: ignore[assignment]
    operation_mode_factor: float = GenOMBCStatus.model_fields["operation_mode_factor"]  # type: ignore[assignment]
