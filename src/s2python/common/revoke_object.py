from pydantic import Field
from typing import Literal

from s2python.generated.gen_s2 import RevokeObject as GenRevokeObject
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class RevokeObject(GenRevokeObject, S2Message["RevokeObject"]):
    class Config(GenRevokeObject.Config):
        validate_assignment = True

    message_type: Literal["RevokeObject"] = Field(default="RevokeObject")
