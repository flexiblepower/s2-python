from typing import List
import uuid

from s2python.generated.gen_s2 import FRBCUsageForecast as GenFRBCUsageForecast
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)
from s2python.frbc.frbc_usage_forecast_element import FRBCUsageForecastElement


@catch_and_convert_exceptions
class FRBCUsageForecast(GenFRBCUsageForecast, S2Message["FRBCUsageForecast"]):
    class Config(GenFRBCUsageForecast.Config):
        validate_assignment = True

    elements: List[FRBCUsageForecastElement] = GenFRBCUsageForecast.__fields__[
        "elements"
    ].field_info  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCUsageForecast.__fields__["message_id"].field_info  # type: ignore[assignment]
