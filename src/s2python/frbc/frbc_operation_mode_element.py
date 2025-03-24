from typing import Optional, List

from s2python.common import NumberRange, PowerRange
from s2python.generated.gen_s2 import (
    FRBCOperationModeElement as GenFRBCOperationModeElement,
)
from s2python.validate_values_mixin import (
    S2MessageComponent,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class FRBCOperationModeElement(GenFRBCOperationModeElement, S2MessageComponent):
    model_config = GenFRBCOperationModeElement.model_config
    model_config["validate_assignment"] = True

    fill_level_range: NumberRange = GenFRBCOperationModeElement.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "fill_level_range"
    ]  # type: ignore[assignment]
    fill_rate: NumberRange = GenFRBCOperationModeElement.model_fields["fill_rate"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    power_ranges: List[PowerRange] = GenFRBCOperationModeElement.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "power_ranges"
    ]  # type: ignore[assignment]
    running_costs: Optional[NumberRange] = GenFRBCOperationModeElement.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "running_costs"
    ]  # type: ignore[assignment]
