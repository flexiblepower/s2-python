from s2python.generated.gen_s2 import PowerValue as GenPowerValue
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class PowerValue(GenPowerValue, S2MessageComponent):
    model_config = GenPowerValue.model_config
    model_config["validate_assignment"] = True
