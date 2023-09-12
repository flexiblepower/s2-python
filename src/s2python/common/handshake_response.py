import uuid

from s2python.generated.gen_s2 import HandshakeResponse as GenHandshakeResponse
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    ValidateValuesMixin,
)


@catch_and_convert_exceptions
class HandshakeResponse(GenHandshakeResponse, ValidateValuesMixin["HandshakeResponse"]):
    class Config(GenHandshakeResponse.Config):
        validate_assignment = True

    message_id: uuid.UUID = GenHandshakeResponse.__fields__["message_id"].field_info  # type: ignore[assignment]
