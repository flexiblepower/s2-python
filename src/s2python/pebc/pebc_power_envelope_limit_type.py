from s2python.generated.gen_s2 import (
    PEBCPowerEnvelopeLimitType as GenPEBCPowerEnvelopeLimitType,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)
from enum import Enum


@catch_and_convert_exceptions
class PEBCPowerEnvelopeLimitType(
    Enum,
    GenPEBCPowerEnvelopeLimitType,
    S2Message["PEBCPowerEnvelopeLimitType"],
):
    pass
