from s2wsjson.generated.gen_s2 import FRBCActuatorDescription as GenFRBCActuatorDescription
from s2wsjson.validate_values_mixin import ValidateValuesMixin


class FRBCActuatorDescription(GenFRBCActuatorDescription, ValidateValuesMixin['FRBCActuatorDescription']):
    class Config(GenFRBCActuatorDescription.Config):
        validate_assignment = True
