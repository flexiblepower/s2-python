import uuid
from typing import Union

from s2python.generated.gen_s2 import (
    PPBCPowerSequenceContainerStatus as GenPPBCPowerSequenceContainerStatus,
)

from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    S2MessageComponent,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class PPBCPowerSequenceContainerStatus(GenPPBCPowerSequenceContainerStatus, S2MessageComponent):
    model_config = copy_config(GenPPBCPowerSequenceContainerStatus.model_config, validate_assignment=True)

    power_profile_id: uuid.UUID = copy_field(GenPPBCPowerSequenceContainerStatus.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "power_profile_id"  # type: ignore[assignment]
    ])
    sequence_container_id: uuid.UUID = copy_field(GenPPBCPowerSequenceContainerStatus.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "sequence_container_id"  # type: ignore[assignment]
    ])
    selected_sequence_id: Union[uuid.UUID, None] = copy_field(GenPPBCPowerSequenceContainerStatus.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "selected_sequence_id"
    ])  # type: ignore[assignment]
    progress: Union[uuid.UUID, None] = copy_field(GenPPBCPowerSequenceContainerStatus.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "progress"  # type: ignore[assignment]
    ])
