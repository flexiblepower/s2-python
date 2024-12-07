from typing import Literal

from pydantic import Field

from s2python.generated.gen_s2 import Handshake as GenHandshake
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class Handshake(GenHandshake, S2Message["Handshake"]):
    class Config(GenHandshake.Config):
        validate_assignment = True

    message_type: Literal["Handshake"] = Field(default="Handshake")
