from s2wsjson.generated.gen_s2 import FRBCUsageForecast as GenFRBCUsageForecast
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCUsageForecast(GenFRBCUsageForecast, ValidateValuesMixin['FRBCUsageForecast']):
    class Config(GenFRBCUsageForecast.Config):
        validate_assignment = True
