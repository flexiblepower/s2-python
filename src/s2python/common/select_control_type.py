from typing import Literal

from pydantic import Field

from s2python.generated.gen_s2 import SelectControlType as GenSelectControlType
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class SelectControlType(GenSelectControlType, S2Message["SelectControlType"]):
    class Config(GenSelectControlType.Config):
        validate_assignment = True

    message_type: Literal["SelectControlType"] = Field(default="SelectControlType")
