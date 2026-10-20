import uuid

from s2python.generated.gen_s2 import SessionRequest as GenSessionRequest
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class SessionRequest(GenSessionRequest, S2MessageComponent):
    model_config = copy_config(GenSessionRequest.model_config, validate_assignment=True)

    message_id: uuid.UUID = copy_field(GenSessionRequest.model_fields["message_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
