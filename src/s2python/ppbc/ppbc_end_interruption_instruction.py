from typing import List
import uuid

from s2python.generated.gen_s2 import (
    PPBCEndInterruptionInstruction as GenPPBCEndInterruptionInstruction,
)

from s2python.validate_values_mixin import (
    S2Message,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class PPBCEndInterruptionInstruction(
    GenPPBCEndInterruptionInstruction, S2Message["PPBCEndInterruptionInstruction"]
):
    model_config = GenPPBCEndInterruptionInstruction.model_config
    model_config["validate_assignment"] = True

    id: uuid.UUID = GenPPBCEndInterruptionInstruction.model_fields["id"]
    power_profile_id: uuid.UUID = GenPPBCEndInterruptionInstruction.model_fields[
        "power_profile_id"
    ]
    sequence_container_id: uuid.UUID = GenPPBCEndInterruptionInstruction.model_fields[
        "sequence_container_id"
    ]
    power_sequence_id: uuid.UUID = GenPPBCEndInterruptionInstruction.model_fields[
        "power_sequence_id"
    ]
    abnormal_condition: bool = GenPPBCEndInterruptionInstruction.model_fields[
        "abnormal_condition"
    ]
