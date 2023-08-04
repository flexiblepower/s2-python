from s2wsjson.common import Duration

from s2wsjson.generated.gen_s2 import FRBCFillLevelTargetProfileElement as GenFRBCFillLevelTargetProfileElement
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCFillLevelTargetProfileElement(GenFRBCFillLevelTargetProfileElement, ValidateValuesMixin['FRBCFillLevelTargetProfileElement']):
    class Config(GenFRBCFillLevelTargetProfileElement.Config):
        validate_assignment = True

    duration: Duration = GenFRBCFillLevelTargetProfileElement.__fields__['duration'].field_info  # type: ignore[assignment]
