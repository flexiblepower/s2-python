from typing import List
import uuid

from s2python.generated.gen_s2 import FRBCUsageForecast as GenFRBCUsageForecast
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)
from s2python.frbc.frbc_usage_forecast_element import FRBCUsageForecastElement


@catch_and_convert_exceptions
class FRBCUsageForecast(GenFRBCUsageForecast, S2MessageComponent):
    model_config = copy_config(GenFRBCUsageForecast.model_config, validate_assignment=True)

    elements: List[FRBCUsageForecastElement] = copy_field(GenFRBCUsageForecast.model_fields["elements"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    message_id: uuid.UUID = copy_field(GenFRBCUsageForecast.model_fields["message_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
