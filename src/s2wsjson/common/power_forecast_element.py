from s2wsjson.generated.gen_s2 import PowerForecastElement as GenPowerForecastElement
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class PowerForecastElement(GenPowerForecastElement, ValidateValuesMixin['PowerForecastElement']):
    class Config(GenPowerForecastElement.Config):
        validate_assignment = True
