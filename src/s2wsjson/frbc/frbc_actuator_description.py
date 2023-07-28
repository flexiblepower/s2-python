from s2wsjson.generated.gen_s2 import FRBCActuatorDescription as GenFRBCActuatorDescription
from s2wsjson.validate_values_mixin import ValidateValuesMixin, catch_and_convert_exceptions


@catch_and_convert_exceptions
class FRBCActuatorDescription(GenFRBCActuatorDescription, ValidateValuesMixin['FRBCActuatorDescription']):
    class Config(GenFRBCActuatorDescription.Config):
        validate_assignment = True
