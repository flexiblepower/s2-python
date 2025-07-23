import uuid
from typing import List, Dict, Tuple
from typing_extensions import Self

from pydantic import model_validator

from s2python.common import CommodityQuantity
from s2python.generated.gen_s2 import (
    PEBCPowerConstraints as GenPEBCPowerConstraints,
    PEBCPowerEnvelopeConsequenceType as GenPEBCPowerEnvelopeConsequenceType,
    PEBCPowerEnvelopeLimitType,
)
from s2python.pebc.pebc_allowed_limit_range import PEBCAllowedLimitRange
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class PEBCPowerConstraints(GenPEBCPowerConstraints, S2MessageComponent):
    model_config = GenPEBCPowerConstraints.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenPEBCPowerConstraints.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    id: uuid.UUID = GenPEBCPowerConstraints.model_fields["id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    consequence_type: GenPEBCPowerEnvelopeConsequenceType = GenPEBCPowerConstraints.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "consequence_type"
    ]  # type: ignore[assignment]
    allowed_limit_ranges: List[PEBCAllowedLimitRange] = GenPEBCPowerConstraints.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "allowed_limit_ranges"
    ]  # type: ignore[assignment]

    @model_validator(mode="after")
    def validate_has_one_upper_one_lower_limit_range(self) -> Self:

        commodity_type_ranges: Dict[CommodityQuantity, Tuple[bool, bool]] = {}

        for limit_range in self.allowed_limit_ranges:
            current: Tuple[bool, bool] = commodity_type_ranges.get(
                limit_range.commodity_quantity, (False, False)
            )

            if limit_range.limit_type == PEBCPowerEnvelopeLimitType.UPPER_LIMIT:
                current = (
                    True,
                    current[1],
                )

            if limit_range.limit_type == PEBCPowerEnvelopeLimitType.LOWER_LIMIT:
                current = (
                    current[0],
                    True,
                )

            commodity_type_ranges[limit_range.commodity_quantity] = current

        valid = True

        for upper, lower in commodity_type_ranges.values():
            valid = valid and upper and lower

        if not valid:
            raise ValueError(
                self,
                "There shall be at least one PEBC.AllowedLimitRange for the UPPER_LIMIT and at least one AllowedLimitRange for the LOWER_LIMIT.",
            )

        return self

    @model_validator(mode="after")
    def validate_valid_until_after_valid_from(self) -> Self:
        if self.valid_until is not None and self.valid_until < self.valid_from:
            raise ValueError(
                self, "valid_until cannot be set to a value that is before valid_from."
            )
        return self
