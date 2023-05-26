from s2wsjson.generated.gen_s2 import PowerRange as GenPowerRange
from s2wsjson.validate_values_mixin import ValidateValuesMixin


class PowerRange(GenPowerRange, ValidateValuesMixin['PowerRange']):
    class Config(GenPowerRange.Config):
        validate_assignment = True
