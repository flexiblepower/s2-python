import uuid

from s2python.generated.gen_s2 import (
    PPBCStartInterruptionInstruction as GenPPBCStartInterruptionInstruction,
)

from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    S2MessageComponent,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class PPBCStartInterruptionInstruction(GenPPBCStartInterruptionInstruction, S2MessageComponent):
    model_config = copy_config(GenPPBCStartInterruptionInstruction.model_config, validate_assignment=True)

    id: uuid.UUID = copy_field(GenPPBCStartInterruptionInstruction.model_fields["id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    message_id: uuid.UUID = copy_field(GenPPBCStartInterruptionInstruction.model_fields["message_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    power_profile_id: uuid.UUID = copy_field(GenPPBCStartInterruptionInstruction.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "power_profile_id"
    ])  # type: ignore[assignment]
    sequence_container_id: uuid.UUID = copy_field(GenPPBCStartInterruptionInstruction.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "sequence_container_id"
    ])  # type: ignore[assignment]
    power_sequence_id: uuid.UUID = copy_field(GenPPBCStartInterruptionInstruction.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "power_sequence_id"
    ])  # type: ignore[assignment]
    abnormal_condition: bool = copy_field(GenPPBCStartInterruptionInstruction.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "abnormal_condition"
    ])  # type: ignore[assignment]
