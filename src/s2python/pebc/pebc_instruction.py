import uuid
from typing import List

from s2python.generated.gen_s2 import (
    PEBCInstruction as GenPEBCInstruction,
)
from s2python.pebc.pebc_power_envelope import PEBCPowerEnvelope
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PEBCInstruction(GenPEBCInstruction, S2Message["PEBCInstruction"]):
    model_config = GenPEBCInstruction.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenPEBCInstruction.model_fields["message_id"]  # type: ignore[assignment]
    id: uuid.UUID = GenPEBCInstruction.model_fields["id"]  # type: ignore[assignment]
    power_constraints_id: uuid.UUID = [
        GenPEBCInstruction.model_fields["power_constraints_id"]  # type: ignore[assignment]
    ]
    power_envelopes: List[PEBCPowerEnvelope] = [
        GenPEBCInstruction.model_fields["power_envelopes"]  # type: ignore[assignment]
    ]
    abnormal_conditions: bool = GenPEBCInstruction.model_fields["abnormal_conditions"]  # type: ignore[assignment]
