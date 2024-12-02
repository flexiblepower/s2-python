from pydantic import Field
from typing import Literal
import uuid

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

    message_id: uuid.UUID = GenInstructionStatusUpdate.__fields__["message_id"].field_info  # type: ignore[assignment]
    instruction_id: uuid.UUID = GenInstructionStatusUpdate.__fields__[
        "instruction_id"
    ].field_info  # type: ignore[assignment]
    message_type: Literal["InstructionStatusUpdate"] = Field(default="InstructionStatusUpdate")
