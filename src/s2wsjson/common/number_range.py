from pydantic import validator

from s2wsjson.s2_validation_error import S2ValidationError
from s2wsjson.validate_values_mixin import ValidateValuesMixin
from s2wsjson.generated.gen_s2 import NumberRange as GenNumberRange


class NumberRange(GenNumberRange, ValidateValuesMixin['NumberRange']):
    class Config(GenNumberRange.Config):
        validate_assignment = True

    @validator('start_of_range')
    def validate_start_of_range(cls, v):
        if v < 0:
            raise ValueError('start_of_range should be >= 0')
        return v

    def validate_across_values(self) -> bool:
        if self.start_of_range > self.end_of_range:
            raise S2ValidationError(self, 'start_of_range should not be higher than end_of_range')

        return True
