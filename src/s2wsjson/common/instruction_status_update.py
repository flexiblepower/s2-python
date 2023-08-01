from s2wsjson.generated.gen_s2 import InstructionStatusUpdate as GenInstructionStatusUpdate
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class InstructionStatusUpdate(GenInstructionStatusUpdate, ValidateValuesMixin['InstructionStatusUpdate']):
    class Config(GenInstructionStatusUpdate.Config):
        validate_assignment = True
