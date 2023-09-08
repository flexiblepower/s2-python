from s2python.generated.gen_s2 import PowerValue as GenPowerValue
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    ValidateValuesMixin,
)


@catch_and_convert_exceptions
class PowerValue(GenPowerValue, ValidateValuesMixin["PowerValue"]):
    class Config(GenPowerValue.Config):
        validate_assignment = True
