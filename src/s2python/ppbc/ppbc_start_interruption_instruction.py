import uuid

from s2python.generated.gen_s2 import (
    PPBCStartInterruptionInstruction as GenPPBCStartInterruptionInstruction,
)

from s2python.validate_values_mixin import (
    S2Message,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class PPBCStartInterruptionInstruction(
    GenPPBCStartInterruptionInstruction, S2Message["PPBCStartInterruptionInstruction"]
):
    model_config = GenPPBCStartInterruptionInstruction.model_config
    model_config["validate_assignment"] = True

    id: uuid.UUID = GenPPBCStartInterruptionInstruction.model_fields["id"]
    power_profile_id: uuid.UUID = GenPPBCStartInterruptionInstruction.model_fields[
        "power_profile_id"
    ]
    sequence_container_id: uuid.UUID = GenPPBCStartInterruptionInstruction.model_fields[
        "sequence_container_id"
    ]
    power_sequence_id: uuid.UUID = GenPPBCStartInterruptionInstruction.model_fields[
        "power_sequence_id"
    ]
    abnormal_condition: bool = GenPPBCStartInterruptionInstruction.model_fields[
        "abnormal_condition"
    ]
