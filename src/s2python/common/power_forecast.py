from typing import List
import uuid

from s2python.common import PowerForecastElement
from s2python.generated.gen_s2 import PowerForecast as GenPowerForecast
from s2python.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class PowerForecast(GenPowerForecast, ValidateValuesMixin['PowerForecast']):
    class Config(GenPowerForecast.Config):
        validate_assignment = True

    message_id: uuid.UUID = GenPowerForecast.__fields__['message_id'].field_info  # type: ignore[assignment]
    elements: List[PowerForecastElement] = GenPowerForecast.__fields__['elements'].field_info  # type: ignore[assignment]
