from s2wsjson.generated.gen_s2 import FRBCOperationMode as GenFRBCOperationMode
from s2wsjson.validate_values_mixin import ValidateValuesMixin


class FRBCOperationMode(GenFRBCOperationMode, ValidateValuesMixin['FRBCOperationMode']):
    class Config(GenFRBCOperationMode.Config):
        validate_assignment = True
