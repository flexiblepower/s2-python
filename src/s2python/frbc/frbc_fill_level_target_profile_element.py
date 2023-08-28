from s2python.common import Duration, NumberRange

from s2python.generated.gen_s2 import FRBCFillLevelTargetProfileElement as GenFRBCFillLevelTargetProfileElement
from s2python.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCFillLevelTargetProfileElement(GenFRBCFillLevelTargetProfileElement, ValidateValuesMixin['FRBCFillLevelTargetProfileElement']):
    class Config(GenFRBCFillLevelTargetProfileElement.Config):
        validate_assignment = True

    duration: Duration = GenFRBCFillLevelTargetProfileElement.__fields__['duration'].field_info  # type: ignore[assignment]
    fill_level_range: NumberRange = GenFRBCFillLevelTargetProfileElement.__fields__['fill_level_range'].field_info  # type: ignore[assignment]
