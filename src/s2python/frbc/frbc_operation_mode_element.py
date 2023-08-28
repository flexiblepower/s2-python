from typing import Optional, List

from s2python.common import NumberRange, PowerRange
from s2python.generated.gen_s2 import FRBCOperationModeElement as GenFRBCOperationModeElement
from s2python.validate_values_mixin import ValidateValuesMixin, catch_and_convert_exceptions


@catch_and_convert_exceptions
class FRBCOperationModeElement(GenFRBCOperationModeElement, ValidateValuesMixin['FRBCOperationModeElement']):
    class Config(GenFRBCOperationModeElement.Config):
        validate_assignment = True

    fill_level_range: NumberRange = GenFRBCOperationModeElement.__fields__['fill_level_range'].field_info  # type: ignore[assignment]
    fill_rate: NumberRange = GenFRBCOperationModeElement.__fields__['fill_rate'].field_info  # type: ignore[assignment]
    power_ranges: List[PowerRange] = GenFRBCOperationModeElement.__fields__['power_ranges'].field_info  # type: ignore[assignment]
    running_costs: Optional[NumberRange] = GenFRBCOperationModeElement.__fields__['running_costs'].field_info  # type: ignore[assignment]
