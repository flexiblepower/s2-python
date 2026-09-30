import uuid

from s2python.generated.gen_s2 import ReceptionStatus as GenReceptionStatus
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class ReceptionStatus(GenReceptionStatus, S2MessageComponent):
    model_config = copy_config(GenReceptionStatus.model_config, validate_assignment=True)

    subject_message_id: uuid.UUID = copy_field(GenReceptionStatus.model_fields["subject_message_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
