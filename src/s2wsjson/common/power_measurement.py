from s2wsjson.generated.gen_s2 import PowerMeasurement as GenPowerMeasurement
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class PowerMeasurement(GenPowerMeasurement, ValidateValuesMixin['PowerMeasurement']):
    class Config(GenPowerMeasurement.Config):
        validate_assignment = True
