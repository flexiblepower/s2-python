import uuid

from s2python.generated.gen_s2 import HandshakeResponse as GenHandshakeResponse
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class HandshakeResponse(GenHandshakeResponse, S2MessageComponent):
    model_config = GenHandshakeResponse.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenHandshakeResponse.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
