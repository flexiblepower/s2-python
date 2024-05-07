from s2python.generated.gen_s2 import FRBCInstruction as GenFRBCInstruction
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class FRBCInstruction(GenFRBCInstruction, S2Message["FRBCInstruction"]):
    class Config(GenFRBCInstruction.Config):
        validate_assignment = True
