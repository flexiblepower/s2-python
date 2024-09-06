from s2python.common import Duration, NumberRange

from s2python.generated.gen_s2 import (
    FRBCFillLevelTargetProfileElement as GenFRBCFillLevelTargetProfileElement,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class FRBCFillLevelTargetProfileElement(
    GenFRBCFillLevelTargetProfileElement,
    S2Message["FRBCFillLevelTargetProfileElement"],
):
    model_config = GenFRBCFillLevelTargetProfileElement.model_config
    model_config["validate_assignment"] = True

    duration: Duration = GenFRBCFillLevelTargetProfileElement.model_fields["duration"]  # type: ignore[assignment]
    fill_level_range: NumberRange = GenFRBCFillLevelTargetProfileElement.model_fields[
        "fill_level_range"
    ]  # type: ignore[assignment]
