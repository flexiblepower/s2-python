import uuid

from s2python.generated.gen_s2 import RevokeObject as GenRevokeObject
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class RevokeObject(GenRevokeObject, S2MessageComponent):
    model_config = GenRevokeObject.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenRevokeObject.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    object_id: uuid.UUID = GenRevokeObject.model_fields["object_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
