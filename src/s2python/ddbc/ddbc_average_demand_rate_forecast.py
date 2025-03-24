from typing import List
import uuid

from s2python.generated.gen_s2 import (
    DDBCAverageDemandRateForecast as GenDDBCAverageDemandRateForecast,
)
from s2python.ddbc.ddbc_average_demand_rate_forecast_element import (
    DDBCAverageDemandRateForecastElement,
)

from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class DDBCAverageDemandRateForecast(
    GenDDBCAverageDemandRateForecast,
    S2MessageComponent,
):
    model_config = GenDDBCAverageDemandRateForecast.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenDDBCAverageDemandRateForecast.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    elements: List[DDBCAverageDemandRateForecastElement] = (  # type: ignore[reportIncompatibleVariableOverride]
        GenDDBCAverageDemandRateForecast.model_fields["elements"]  # type: ignore[assignment]
    )
