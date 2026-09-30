import uuid

from s2python.generated.gen_s2 import SelectControlType as GenSelectControlType
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class SelectControlType(GenSelectControlType, S2MessageComponent):
    model_config = copy_config(GenSelectControlType.model_config, validate_assignment=True)

    message_id: uuid.UUID = copy_field(GenSelectControlType.model_fields["message_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
