from typing import List
import uuid

from s2python.common.power_value import PowerValue
from s2python.generated.gen_s2 import PowerMeasurement as GenPowerMeasurement
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PowerMeasurement(GenPowerMeasurement, S2Message["PowerMeasurement"]):
    model_config = GenPowerMeasurement.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenPowerMeasurement.model_fields["message_id"]  # type: ignore[assignment]
    values: List[PowerValue] = GenPowerMeasurement.model_fields["values"]  # type: ignore[assignment]
