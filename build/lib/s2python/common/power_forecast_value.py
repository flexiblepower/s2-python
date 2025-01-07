from s2python.generated.gen_s2 import PowerForecastValue as GenPowerForecastValue
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PowerForecastValue(GenPowerForecastValue, S2Message["PowerForecastValue"]):
    model_config = GenPowerForecastValue.model_config
    model_config["validate_assignment"] = True
