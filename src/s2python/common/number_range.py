from typing import Any, Dict

from pydantic import root_validator

from s2python.generated.gen_s2 import NumberRange as GenNumberRange
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class NumberRange(GenNumberRange, S2Message["NumberRange"]):
    class Config(GenNumberRange.Config):
        validate_assignment = True

    @root_validator(pre=False)
    @classmethod
    def validate_start_end_order(  # pylint: disable=duplicate-code
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        if values.get("start_of_range", 0.0) > values.get("end_of_range", 0.0):
            raise ValueError(
                cls, "start_of_range should not be higher than end_of_range"
            )

        return values

    def __hash__(self) -> int:
        return hash(f"{self.start_of_range}|{self.end_of_range}")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, NumberRange):
            return (
                self.start_of_range == other.start_of_range
                and self.end_of_range == other.end_of_range
            )

        return False
