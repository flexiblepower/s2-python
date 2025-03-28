from typing import List

from s2python.generated.gen_s2 import PowerForecastElement as GenPowerForecastElement
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)
from s2python.common.duration import Duration
from s2python.common.power_forecast_value import PowerForecastValue


@catch_and_convert_exceptions
class PowerForecastElement(GenPowerForecastElement, S2MessageComponent):
    model_config = GenPowerForecastElement.model_config
    model_config["validate_assignment"] = True

    duration: Duration = GenPowerForecastElement.model_fields["duration"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    power_values: List[PowerForecastValue] = (  # type: ignore[reportIncompatibleVariableOverride]
        GenPowerForecastElement.model_fields["power_values"]  # type: ignore[assignment]
    )
