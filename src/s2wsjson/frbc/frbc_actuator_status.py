from s2wsjson.generated.gen_s2 import FRBCActuatorStatus as GenFRBCActuatorStatus
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCActuatorStatus(GenFRBCActuatorStatus, ValidateValuesMixin['FRBCActuatorStatus']):
    class Config(GenFRBCActuatorStatus.Config):
        validate_assignment = True
