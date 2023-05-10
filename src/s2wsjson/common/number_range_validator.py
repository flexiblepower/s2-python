from pydantic import validator

from s2wsjson.generated.gen_s2 import NumberRange as GenNumberRange


class NumberRangeValidator(GenNumberRange):
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
