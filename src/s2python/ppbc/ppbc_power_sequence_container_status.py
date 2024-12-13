from typing import List
import uuid

from s2python.generated.gen_s2 import (
    PPBCPowerSequenceContainerStatus as GenPPBCPowerSequenceContainerStatus,
)

from s2python.validate_values_mixin import (
    S2Message,
    catch_and_convert_exceptions,
)
from s2python.common import Duration


@catch_and_convert_exceptions
class PPBCPowerProfileDefinitionStatus(
    GenPPBCPowerSequenceContainerStatus, S2Message["PPBCPowerProfileDefinitionStatus"]
):
    model_config = GenPPBCPowerSequenceContainerStatus.model_config
    model_config["validate_assignment"] = True

    power_profile_id: uuid.UUID = GenPPBCPowerSequenceContainerStatus.model_fields["id"]
    sequence_container_id: uuid.UUID = GenPPBCPowerSequenceContainerStatus.model_fields[
        "sequence_container_id"
    ]
    selected_sequence_id: uuid.UUID | None = (
        GenPPBCPowerSequenceContainerStatus.model_fields["selected_sequence_id"]
    )
    progress: Duration | None = GenPPBCPowerSequenceContainerStatus.model_fields[
        "progress"
    ]
