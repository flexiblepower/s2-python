from typing import Literal

from pydantic import Field

from s2python.generated.gen_s2 import HandshakeResponse as GenHandshakeResponse
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class HandshakeResponse(GenHandshakeResponse, S2Message["HandshakeResponse"]):
    class Config(GenHandshakeResponse.Config):
        validate_assignment = True

    message_type: Literal["HandshakeResponse"] = Field(default="HandshakeResponse")
