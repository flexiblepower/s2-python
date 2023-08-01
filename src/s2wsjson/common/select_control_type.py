from s2wsjson.generated.gen_s2 import SelectControlType as GenSelectControlType
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class SelectControlType(GenSelectControlType, ValidateValuesMixin['SelectControlType']):
    class Config(GenSelectControlType.Config):
        validate_assignment = True
