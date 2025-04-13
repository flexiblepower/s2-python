from typing import List
import uuid


from s2python.generated.gen_s2 import (
    PPBCPowerSequenceContainer as GenPPBCPowerSequenceContainer,
)

from s2python.validate_values_mixin import (
    S2MessageComponent,
    catch_and_convert_exceptions,
)

from s2python.ppbc.ppbc_power_sequence import PPBCPowerSequence


@catch_and_convert_exceptions
class PPBCPowerSequenceContainer(GenPPBCPowerSequenceContainer, S2MessageComponent):
    model_config = GenPPBCPowerSequenceContainer.model_config
    model_config["validate_assignment"] = True

    id: uuid.UUID = GenPPBCPowerSequenceContainer.model_fields["id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    power_sequences: List[PPBCPowerSequence] = GenPPBCPowerSequenceContainer.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "power_sequences"
    ]  # type: ignore[assignment]
