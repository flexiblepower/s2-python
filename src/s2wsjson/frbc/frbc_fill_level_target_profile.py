from typing import List

from s2wsjson.frbc import FRBCFillLevelTargetProfileElement
from s2wsjson.generated.gen_s2 import FRBCFillLevelTargetProfile as GenFRBCFillLevelTargetProfile
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCFillLevelTargetProfile(GenFRBCFillLevelTargetProfile, ValidateValuesMixin['FRBCFillLevelTargetProfile']):
    class Config(GenFRBCFillLevelTargetProfile.Config):
        validate_assignment = True

    elements: List[FRBCFillLevelTargetProfileElement] = GenFRBCFillLevelTargetProfile.__fields__['elements'].field_info  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCFillLevelTargetProfile.__fields__['message_id'].field_info  # type: ignore[assignment]
