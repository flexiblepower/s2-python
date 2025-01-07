import uuid

from s2python.generated.gen_s2 import (
    InstructionStatusUpdate as GenInstructionStatusUpdate,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class InstructionStatusUpdate(GenInstructionStatusUpdate, S2Message["InstructionStatusUpdate"]):
    model_config = GenInstructionStatusUpdate.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenInstructionStatusUpdate.model_fields["message_id"]  # type: ignore[assignment]
    instruction_id: uuid.UUID = GenInstructionStatusUpdate.model_fields["instruction_id"]  # type: ignore[assignment]
