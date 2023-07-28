from pydantic import root_validator

from s2wsjson.generated.gen_s2 import PowerRange as GenPowerRange
from s2wsjson.validate_values_mixin import ValidateValuesMixin, catch_and_convert_exceptions


@catch_and_convert_exceptions
class PowerRange(GenPowerRange, ValidateValuesMixin['PowerRange']):
    class Config(GenPowerRange.Config):
        validate_assignment = True

    @root_validator(pre=False)
    def validate_start_end_order(cls, values):
        if values.get("start_of_range") > values.get("end_of_range"):
            raise ValueError(cls, 'start_of_range should not be higher than end_of_range')

        return values
