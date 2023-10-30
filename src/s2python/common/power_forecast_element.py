from typing import List

from s2python.generated.gen_s2 import PowerForecastElement as GenPowerForecastElement
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)
from s2python.common.duration import Duration
from s2python.common.power_forecast_value import PowerForecastValue


@catch_and_convert_exceptions
class PowerForecastElement(GenPowerForecastElement, S2Message["PowerForecastElement"]):
    class Config(GenPowerForecastElement.Config):
        validate_assignment = True

    duration: Duration = GenPowerForecastElement.__fields__["duration"].field_info  # type: ignore[assignment]
    power_values: List[PowerForecastValue] = GenPowerForecastElement.__fields__[
        "power_values"
    ].field_info  # type: ignore[assignment]
