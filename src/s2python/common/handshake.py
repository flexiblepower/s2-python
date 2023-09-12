import uuid

from s2python.generated.gen_s2 import Handshake as GenHandshake
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    ValidateValuesMixin,
)


@catch_and_convert_exceptions
class Handshake(GenHandshake, ValidateValuesMixin["Handshake"]):
    class Config(GenHandshake.Config):
        validate_assignment = True

    message_id: uuid.UUID = GenHandshake.__fields__["message_id"].field_info  # type: ignore[assignment]
