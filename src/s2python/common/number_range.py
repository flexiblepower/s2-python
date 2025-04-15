from typing import Any

from s2python.validate_values_mixin import (
    S2MessageComponent,
    catch_and_convert_exceptions,
)
from s2python.generated.gen_s2 import NumberRange as GenNumberRange


@catch_and_convert_exceptions
class NumberRange(GenNumberRange, S2MessageComponent):
    model_config = GenNumberRange.model_config
    model_config["validate_assignment"] = True

    def __hash__(self) -> int:
        return hash(f"{self.start_of_range}|{self.end_of_range}")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, NumberRange):
            return (
                self.start_of_range == other.start_of_range
                and self.end_of_range == other.end_of_range
            )

        return False
