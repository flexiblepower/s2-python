from s2python.generated.gen_s2 import (
    PEBCAllowedLimitRange as GenPEBCAllowedLimitRange,
    PEBCPowerEnvelopeLimitType as GenPEBCPowerEnvelopeLimitType,
)
from s2python.common import CommodityQuantity, NumberRange
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class PEBCAllowedLimitRange(GenPEBCAllowedLimitRange, S2MessageComponent):
    model_config = GenPEBCAllowedLimitRange.model_config
    model_config["validate_assignment"] = True

    commodity_quantity: CommodityQuantity = GenPEBCAllowedLimitRange.model_fields[
        "commodity_quantity"
    ]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    limit_type: GenPEBCPowerEnvelopeLimitType = GenPEBCAllowedLimitRange.model_fields[
        "limit_type"
    ]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    range_boundary: NumberRange = GenPEBCAllowedLimitRange.model_fields["range_boundary"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    abnormal_condition_only: bool = [
        GenPEBCAllowedLimitRange.model_fields["abnormal_condition_only"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    ]
