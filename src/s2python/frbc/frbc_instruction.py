import uuid

from s2python.generated.gen_s2 import FRBCInstruction as GenFRBCInstruction
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class FRBCInstruction(GenFRBCInstruction, S2Message["FRBCInstruction"]):
    model_config = GenFRBCInstruction.model_config
    model_config["validate_assignment"] = True

    actuator_id: uuid.UUID = GenFRBCInstruction.model_fields["actuator_id"]  # type: ignore[assignment]
    id: uuid.UUID = GenFRBCInstruction.model_fields["id"]  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCInstruction.model_fields["message_id"]  # type: ignore[assignment]
    operation_mode: uuid.UUID = GenFRBCInstruction.model_fields["operation_mode"]  # type: ignore[assignment]
