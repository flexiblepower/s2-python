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
    S2Message,
)


@catch_and_convert_exceptions
class DDBCAverageDemandRateForecast(
    GenDDBCAverageDemandRateForecast, S2Message["DDBCAverageDemandRateForecast"]
):
    model_config = GenDDBCAverageDemandRateForecast.model_config
    model_config["validate_assignment"] = True

    elements: List[DDBCAverageDemandRateForecastElement] = (
        GenDDBCAverageDemandRateForecast.model_fields["elements"]
    )
