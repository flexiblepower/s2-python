from typing import List, Literal

from pydantic import Field

from s2python.frbc.frbc_usage_forecast_element import FRBCUsageForecastElement
from s2python.generated.gen_s2 import FRBCUsageForecast as GenFRBCUsageForecast
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class FRBCUsageForecast(GenFRBCUsageForecast, S2Message["FRBCUsageForecast"]):
    class Config(GenFRBCUsageForecast.Config):
        validate_assignment = True

    elements: List[FRBCUsageForecastElement] = GenFRBCUsageForecast.__fields__[
        "elements"
    ].field_info  # type: ignore[assignment]
    message_type: Literal["FRBC.UsageForecast"] = Field(default="FRBC.UsageForecast")
