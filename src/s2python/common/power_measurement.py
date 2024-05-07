from typing import List


from s2python.common.power_value import PowerValue
from s2python.generated.gen_s2 import PowerMeasurement as GenPowerMeasurement
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PowerMeasurement(GenPowerMeasurement, S2Message["PowerMeasurement"]):
    class Config(GenPowerMeasurement.Config):
        validate_assignment = True

    values: List[PowerValue] = GenPowerMeasurement.__fields__["values"].field_info  # type: ignore[assignment]
