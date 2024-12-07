from typing import Literal

from pydantic import Field

from s2python.generated.gen_s2 import (
    InstructionStatusUpdate as GenInstructionStatusUpdate,
)
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class InstructionStatusUpdate(
    GenInstructionStatusUpdate, S2Message["InstructionStatusUpdate"]
):
    class Config(GenInstructionStatusUpdate.Config):
        validate_assignment = True

    message_type: Literal["InstructionStatusUpdate"] = Field(
        default="InstructionStatusUpdate"
    )
