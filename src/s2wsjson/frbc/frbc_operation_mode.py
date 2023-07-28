from s2wsjson.generated.gen_s2 import FRBCOperationMode as GenFRBCOperationMode
from s2wsjson.validate_values_mixin import ValidateValuesMixin, catch_and_convert_exceptions


@catch_and_convert_exceptions
class FRBCOperationMode(GenFRBCOperationMode, ValidateValuesMixin['FRBCOperationMode']):
    class Config(GenFRBCOperationMode.Config):
        validate_assignment = True
