import uuid
from typing import Union

from s2python.generated.gen_s2 import (
    PPBCPowerSequenceContainerStatus as GenPPBCPowerSequenceContainerStatus,
)

from s2python.validate_values_mixin import (
    S2Message,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class PPBCPowerSequenceContainerStatus(
    GenPPBCPowerSequenceContainerStatus, S2Message["PPBCPowerSequenceContainerStatus"]
):
    model_config = GenPPBCPowerSequenceContainerStatus.model_config
    model_config["validate_assignment"] = True

    power_profile_id: uuid.UUID = GenPPBCPowerSequenceContainerStatus.model_fields[
        "power_profile_id"  # type: ignore[assignment]
    ]
    sequence_container_id: uuid.UUID = GenPPBCPowerSequenceContainerStatus.model_fields[
        "sequence_container_id"  # type: ignore[assignment]
    ]
    selected_sequence_id: Union[uuid.UUID, None] = (
        GenPPBCPowerSequenceContainerStatus.model_fields["selected_sequence_id"]  # type: ignore[assignment]
    )
    progress: Union[uuid.UUID, None] = GenPPBCPowerSequenceContainerStatus.model_fields[
        "progress"  # type: ignore[assignment]
    ]
