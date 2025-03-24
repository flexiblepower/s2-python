from typing import List

from s2python.generated.gen_s2 import (
    PPBCPowerProfileStatus as GenPPBCPowerProfileStatus,
)

from s2python.validate_values_mixin import (
    S2MessageComponent,
    catch_and_convert_exceptions,
)

from s2python.ppbc.ppbc_power_sequence_container_status import (
    PPBCPowerSequenceContainerStatus,
)


@catch_and_convert_exceptions
class PPBCPowerProfileStatus(GenPPBCPowerProfileStatus, S2MessageComponent):
    model_config = GenPPBCPowerProfileStatus.model_config
    model_config["validate_assignment"] = True

    sequence_container_status: List[PPBCPowerSequenceContainerStatus] = (  # type: ignore[reportIncompatibleVariableOverride]
        GenPPBCPowerProfileStatus.model_fields["sequence_container_status"]  # type: ignore[assignment]
    )
