# pylint: disable=duplicate-code

from typing_extensions import Self

from pydantic import model_validator

from s2python.common import Duration, NumberRange
from s2python.generated.gen_s2 import (
    FRBCFillLevelTargetProfileElement as GenFRBCFillLevelTargetProfileElement,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class FRBCFillLevelTargetProfileElement(GenFRBCFillLevelTargetProfileElement, S2MessageComponent):
    model_config = GenFRBCFillLevelTargetProfileElement.model_config
    model_config["validate_assignment"] = True

    duration: Duration = GenFRBCFillLevelTargetProfileElement.model_fields["duration"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    fill_level_range: NumberRange = GenFRBCFillLevelTargetProfileElement.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "fill_level_range"
    ]  # type: ignore[assignment]

    @model_validator(mode="after")
    def validate_start_end_order(self) -> Self:
        if self.fill_level_range.start_of_range > self.fill_level_range.end_of_range:
            raise ValueError(
                self,
                "start_of_range should not be higher than end_of_range for the fill_level_range",
            )

        return self
