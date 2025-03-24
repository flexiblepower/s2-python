from typing import List
import uuid

from s2python.frbc.frbc_fill_level_target_profile_element import (
    FRBCFillLevelTargetProfileElement,
)
from s2python.generated.gen_s2 import (
    FRBCFillLevelTargetProfile as GenFRBCFillLevelTargetProfile,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class FRBCFillLevelTargetProfile(GenFRBCFillLevelTargetProfile, S2MessageComponent):
    model_config = GenFRBCFillLevelTargetProfile.model_config
    model_config["validate_assignment"] = True

    elements: List[FRBCFillLevelTargetProfileElement] = GenFRBCFillLevelTargetProfile.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "elements"
    ]  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCFillLevelTargetProfile.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
