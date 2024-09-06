from typing import Optional, List

from s2python.common import NumberRange, PowerRange
from s2python.generated.gen_s2 import (
    FRBCOperationModeElement as GenFRBCOperationModeElement,
)
from s2python.validate_values_mixin import (
    S2Message,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class FRBCOperationModeElement(GenFRBCOperationModeElement, S2Message["FRBCOperationModeElement"]):
    model_config = GenFRBCOperationModeElement.model_config
    model_config["validate_assignment"] = True

    fill_level_range: NumberRange = GenFRBCOperationModeElement.model_fields[
        "fill_level_range"
    ]  # type: ignore[assignment]
    fill_rate: NumberRange = GenFRBCOperationModeElement.model_fields["fill_rate"]  # type: ignore[assignment]
    power_ranges: List[PowerRange] = GenFRBCOperationModeElement.model_fields[
        "power_ranges"
    ]  # type: ignore[assignment]
    running_costs: Optional[NumberRange] = GenFRBCOperationModeElement.model_fields[
        "running_costs"
    ]  # type: ignore[assignment]
