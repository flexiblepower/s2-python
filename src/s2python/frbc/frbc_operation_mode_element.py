from typing import Optional, List

from s2python.common import NumberRange, PowerRange
from s2python.generated.gen_s2 import (
    FRBCOperationModeElement as GenFRBCOperationModeElement,
)
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    S2MessageComponent,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class FRBCOperationModeElement(GenFRBCOperationModeElement, S2MessageComponent):
    model_config = copy_config(GenFRBCOperationModeElement.model_config, validate_assignment=True)

    fill_level_range: NumberRange = copy_field(GenFRBCOperationModeElement.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "fill_level_range"
    ])  # type: ignore[assignment]
    fill_rate: NumberRange = copy_field(GenFRBCOperationModeElement.model_fields["fill_rate"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    power_ranges: List[PowerRange] = copy_field(GenFRBCOperationModeElement.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "power_ranges"
    ])  # type: ignore[assignment]
    running_costs: Optional[NumberRange] = copy_field(GenFRBCOperationModeElement.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "running_costs"
    ])  # type: ignore[assignment]
