from pydantic import validator, root_validator

from s2wsjson.validate_values_mixin import ValidateValuesMixin, patch
from s2wsjson.generated.gen_s2 import NumberRange as GenNumberRange

@patch
class NumberRange(GenNumberRange, ValidateValuesMixin['NumberRange']):
    class Config(GenNumberRange.Config):
        validate_assignment = True

    @validator('start_of_range')
    def validate_start_of_range(cls, v):
        if v < 0:
            raise ValueError('start_of_range should be >= 0')
        return v

    @validator('end_of_range')
    def validate_values(cls, end_of_range, values) -> bool:
        if 'start_of_range' in values and values['start_of_range'] > end_of_range:
            raise ValueError('start_of_range should not be higher than end_of_range')

        return end_of_range

    @root_validator(pre=False)
    def validate_start_end_order(cls, values):
        if values.get("start_of_range") > values.get("end_of_range"):
            raise ValueError(cls, 'start_of_range should not be higher than end_of_range')

        return values
