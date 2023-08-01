from s2wsjson.generated.gen_s2 import FRBCTimerStatus as GenFRBCTimerStatus
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCTimerStatus(GenFRBCTimerStatus, ValidateValuesMixin['FRBCTimerStatus']):
    class Config(GenFRBCTimerStatus.Config):
        validate_assignment = True
