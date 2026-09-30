from typing import List
import uuid

from s2python.common.power_forecast_element import PowerForecastElement
from s2python.generated.gen_s2 import PowerForecast as GenPowerForecast
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class PowerForecast(GenPowerForecast, S2MessageComponent):
    model_config = copy_config(GenPowerForecast.model_config, validate_assignment=True)

    message_id: uuid.UUID = copy_field(GenPowerForecast.model_fields["message_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    elements: List[PowerForecastElement] = copy_field(GenPowerForecast.model_fields["elements"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
