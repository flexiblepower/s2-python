from pydantic import Field
from typing import Literal

from s2python.generated.gen_s2 import SessionRequest as GenSessionRequest
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class SessionRequest(GenSessionRequest, S2Message["SessionRequest"]):
    class Config(GenSessionRequest.Config):
        validate_assignment = True

    message_type: Literal["SessionRequest"] = Field(default="SessionRequest")
