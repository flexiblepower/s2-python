from typing import Any
from typing_extensions import Self

from pydantic import model_validator

from s2python.validate_values_mixin import (
    S2Message,
    catch_and_convert_exceptions,
)
from s2python.generated.gen_s2 import NumberRange as GenNumberRange


@catch_and_convert_exceptions
class NumberRange(GenNumberRange, S2Message["NumberRange"]):
    model_config = GenNumberRange.model_config
    model_config["validate_assignment"] = True

    @model_validator(mode="after")
    def validate_start_end_order(self) -> Self:  # pylint: disable=duplicate-code
        if self.start_of_range > self.end_of_range:
            raise ValueError(self, "start_of_range should not be higher than end_of_range")

        return self

    def __hash__(self) -> int:
        return hash(f"{self.start_of_range}|{self.end_of_range}")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, NumberRange):
            return self.start_of_range == other.start_of_range and self.end_of_range == other.end_of_range

        return False
