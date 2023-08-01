from s2wsjson.generated.gen_s2 import PowerForecast as GenPowerForecast
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class PowerForecast(GenPowerForecast, ValidateValuesMixin['PowerForecast']):
    class Config(GenPowerForecast.Config):
        validate_assignment = True
