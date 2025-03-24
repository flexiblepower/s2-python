from typing import List
import uuid

from s2python.generated.gen_s2 import (
    PPBCPowerSequence as GenPPBCPowerSequence,
)

from s2python.validate_values_mixin import (
    S2MessageComponent,
    catch_and_convert_exceptions,
)

from s2python.ppbc.ppbc_power_sequence_element import PPBCPowerSequenceElement
from s2python.common import Duration


@catch_and_convert_exceptions
class PPBCPowerSequence(GenPPBCPowerSequence, S2MessageComponent):
    model_config = GenPPBCPowerSequence.model_config
    model_config["validate_assignment"] = True

    id: uuid.UUID = GenPPBCPowerSequence.model_fields["id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    elements: List[PPBCPowerSequenceElement] = GenPPBCPowerSequence.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "elements"
    ]  # type: ignore[assignment]
    is_interruptible: bool = GenPPBCPowerSequence.model_fields["is_interruptible"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    max_pause_before: Duration = GenPPBCPowerSequence.model_fields["max_pause_before"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    abnormal_condition_only: bool = GenPPBCPowerSequence.model_fields[
        "abnormal_condition_only"
    ]  # type: ignore[assignment,reportIncompatibleVariableOverride]
