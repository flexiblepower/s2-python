import uuid

from s2python.generated.gen_s2 import SessionRequest as GenSessionRequest
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class SessionRequest(GenSessionRequest, S2MessageComponent):
    model_config = GenSessionRequest.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenSessionRequest.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
