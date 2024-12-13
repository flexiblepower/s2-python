from typing import List
import uuid

from s2python.generated.gen_s2 import (
    PPBCPowerSequence as GenPPBCPowerSequence,
)

from s2python.validate_values_mixin import (
    S2Message,
    catch_and_convert_exceptions,
)

from s2python.ppbc.ppbc_power_sequence_element import PPBCPowerSequenceElement
from s2python.common import Duration


@catch_and_convert_exceptions
class PPBCPowerSequenceContainer(
    GenPPBCPowerSequence, S2Message["PPBCPowerSequenceContainer"]
):
    model_config = GenPPBCPowerSequence.model_config
    model_config["validate_assignment"] = True

    id: uuid.UUID = GenPPBCPowerSequence.model_fields["id"]
    elements: List[PPBCPowerSequenceElement] = GenPPBCPowerSequence.model_fields[
        "elements"
    ]
    is_interruptible: bool = GenPPBCPowerSequence.model_fields["is_interruptible"]
    max_pause_before: Duration = GenPPBCPowerSequence.model_fields["max_pause_before"]
    abnormal_condition_only: bool = GenPPBCPowerSequence.model_fields[
        "abnormal_condition_only"
    ]
