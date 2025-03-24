from typing import List
import uuid

from s2python.generated.gen_s2 import (
    PPBCPowerProfileDefinition as GenPPBCPowerProfileDefinition,
)

from s2python.validate_values_mixin import (
    S2MessageComponent,
    catch_and_convert_exceptions,
)

from s2python.ppbc.ppbc_power_sequence_container import PPBCPowerSequenceContainer


@catch_and_convert_exceptions
class PPBCPowerProfileDefinition(GenPPBCPowerProfileDefinition, S2MessageComponent):
    model_config = GenPPBCPowerProfileDefinition.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenPPBCPowerProfileDefinition.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    id: uuid.UUID = GenPPBCPowerProfileDefinition.model_fields["id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    power_sequences_containers: List[PPBCPowerSequenceContainer] = (  # type: ignore[reportIncompatibleVariableOverride]
        GenPPBCPowerProfileDefinition.model_fields["power_sequences_containers"]  # type: ignore[assignment]
    )
