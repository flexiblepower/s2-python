import uuid

from s2python.generated.gen_s2 import Handshake as GenHandshake
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class Handshake(GenHandshake, S2MessageComponent):
    model_config = GenHandshake.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenHandshake.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
