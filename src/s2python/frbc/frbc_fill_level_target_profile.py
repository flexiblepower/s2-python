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
    S2Message,
)


@catch_and_convert_exceptions
class FRBCFillLevelTargetProfile(
    GenFRBCFillLevelTargetProfile, S2Message["FRBCFillLevelTargetProfile"]
):
    class Config(GenFRBCFillLevelTargetProfile.Config):
        validate_assignment = True

    elements: List[
        FRBCFillLevelTargetProfileElement
    ] = GenFRBCFillLevelTargetProfile.__fields__[
        "elements"
    ].field_info  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCFillLevelTargetProfile.__fields__[
        "message_id"
    ].field_info  # type: ignore[assignment]
