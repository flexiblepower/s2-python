from typing import List
import uuid

from s2python.common.power_forecast_element import PowerForecastElement
from s2python.generated.gen_s2 import PowerForecast as GenPowerForecast
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PowerForecast(GenPowerForecast, S2Message["PowerForecast"]):
    model_config = GenPowerForecast.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenPowerForecast.model_fields["message_id"]  # type: ignore[assignment]
    elements: List[PowerForecastElement] = GenPowerForecast.model_fields["elements"]  # type: ignore[assignment]
