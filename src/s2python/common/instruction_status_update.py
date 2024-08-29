from s2python.generated.gen_s2 import (
    InstructionStatusUpdate as GenInstructionStatusUpdate,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class InstructionStatusUpdate(
    GenInstructionStatusUpdate, S2Message["InstructionStatusUpdate"]
):
    class Config(GenInstructionStatusUpdate.Config):
        validate_assignment = True
