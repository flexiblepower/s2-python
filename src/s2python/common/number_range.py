from typing import Any

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
    @classmethod
    def validate_start_end_order(cls, number_range: "NumberRange") -> "NumberRange":  # pylint: disable=duplicate-code
        if number_range.start_of_range > number_range.end_of_range:
            raise ValueError(cls, "start_of_range should not be higher than end_of_range")

        return number_range

    def __hash__(self) -> int:
        return hash(f"{self.start_of_range}|{self.end_of_range}")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, NumberRange):
            return self.start_of_range == other.start_of_range and self.end_of_range == other.end_of_range

        return False
