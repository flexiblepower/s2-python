from s2wsjson.generated.gen_s2 import FRBCInstruction as GenFRBCInstruction
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCInstruction(GenFRBCInstruction, ValidateValuesMixin['FRBCInstruction']):
    class Config(GenFRBCInstruction.Config):
        validate_assignment = True
