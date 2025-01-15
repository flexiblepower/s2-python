# pylint: disable=duplicate-code

from pydantic import model_validator
from typing_extensions import Self

from s2python.common import NumberRange
from s2python.generated.gen_s2 import FRBCLeakageBehaviourElement as GenFRBCLeakageBehaviourElement
from s2python.validate_values_mixin import catch_and_convert_exceptions, S2Message


@catch_and_convert_exceptions
class FRBCLeakageBehaviourElement(
    GenFRBCLeakageBehaviourElement, S2Message["FRBCLeakageBehaviourElement"]
):
    model_config = GenFRBCLeakageBehaviourElement.model_config
    model_config["validate_assignment"] = True

    fill_level_range: NumberRange = GenFRBCLeakageBehaviourElement.model_fields[
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
