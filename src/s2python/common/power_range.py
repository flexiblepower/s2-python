from typing_extensions import Self

from pydantic import model_validator

from s2python.generated.gen_s2 import PowerRange as GenPowerRange
from s2python.validate_values_mixin import (
    S2Message,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class PowerRange(GenPowerRange, S2Message["PowerRange"]):
    model_config = GenPowerRange.model_config
    model_config["validate_assignment"] = True

    @model_validator(mode="after")
    def validate_start_end_order(self) -> Self:
        if self.start_of_range > self.end_of_range:
            raise ValueError(self, "start_of_range should not be higher than end_of_range")

        return self
