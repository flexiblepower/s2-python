from s2python.generated.gen_s2 import PowerForecastValue as GenPowerForecastValue
from s2python.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class PowerForecastValue(GenPowerForecastValue, ValidateValuesMixin['PowerForecastValue']):
    class Config(GenPowerForecastValue.Config):
        validate_assignment = True
