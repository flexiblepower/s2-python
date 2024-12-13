import uuid

from s2python.generated.gen_s2 import (
    PPBCScheduleInstruction as GenPPBCScheduleInstruction,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PPBCScheduleInstruction(
    GenPPBCScheduleInstruction, S2Message["PPBCScheduleInstruction"]
):
    model_config = GenPPBCScheduleInstruction.model_config
    model_config["validate_assignment"] = True

    id: uuid.UUID = GenPPBCScheduleInstruction.model_fields["id"]  # type: ignore[assignment]

    power_profile_id: uuid.UUID = GenPPBCScheduleInstruction.model_fields[
        "power_profile_id"
    ]  # type: ignore[assignment]

    message_id: uuid.UUID = GenPPBCScheduleInstruction.model_fields["message_id"]  # type: ignore[assignment]

    sequence_container_id: uuid.UUID = GenPPBCScheduleInstruction.model_fields[
        "sequence_container_id"
    ]  # type: ignore[assignment]

    power_sequence_id: uuid.UUID = GenPPBCScheduleInstruction.model_fields[
        "power_sequence_id"
    ]  # type: ignore[assignment]
