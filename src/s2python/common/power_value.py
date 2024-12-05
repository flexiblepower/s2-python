from pydantic import Field
from typing import Literal

from s2python.generated.gen_s2 import PowerValue as GenPowerValue
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PowerValue(GenPowerValue, S2Message["PowerValue"]):
    class Config(GenPowerValue.Config):
        validate_assignment = True
