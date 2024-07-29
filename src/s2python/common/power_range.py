from typing import Any, Dict

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
    @classmethod
    def validate_start_end_order(cls, power_range: "PowerRange") -> "PowerRange":  # pylint: disable=duplicate-code
        if power_range.start_of_range > power_range.end_of_range:
            raise ValueError(cls, "start_of_range should not be higher than end_of_range")

        return power_range
