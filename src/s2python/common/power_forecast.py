from typing import List


from s2python.common.power_forecast_element import PowerForecastElement
from s2python.generated.gen_s2 import PowerForecast as GenPowerForecast
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PowerForecast(GenPowerForecast, S2Message["PowerForecast"]):
    class Config(GenPowerForecast.Config):
        validate_assignment = True

    elements: List[PowerForecastElement] = GenPowerForecast.__fields__[
        "elements"
    ].field_info  # type: ignore[assignment]
