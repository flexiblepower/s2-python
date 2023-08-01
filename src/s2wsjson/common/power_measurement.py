from typing import List

from s2wsjson.common import PowerValue
from s2wsjson.generated.gen_s2 import PowerMeasurement as GenPowerMeasurement
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class PowerMeasurement(GenPowerMeasurement, ValidateValuesMixin['PowerMeasurement']):
    class Config(GenPowerMeasurement.Config):
        validate_assignment = True

    message_id: uuid.UUID = GenPowerMeasurement.__fields__['message_id'].field_info  # type: ignore[assignment]
    values: List[PowerValue] = GenPowerMeasurement.__fields__['values'].field_info  # type: ignore[assignment]
