import uuid
from typing import List, Dict
from typing_extensions import Self

from pydantic import model_validator
from s2python.common.power_value import PowerValue
from s2python.generated.gen_s2 import (
    PowerMeasurement as GenPowerMeasurement,
    CommodityQuantity,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class PowerMeasurement(GenPowerMeasurement, S2MessageComponent):
    model_config = GenPowerMeasurement.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenPowerMeasurement.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    values: List[PowerValue] = GenPowerMeasurement.model_fields["values"]  # type: ignore[assignment,reportIncompatibleVariableOverride]

    @model_validator(mode="after")
    def validate_values_at_most_one_per_commodity_quantity(self) -> Self:
        """Validates the power measurement values to check that there is at most 1 PowerValue per CommodityQuantity."""

        has_value: Dict[CommodityQuantity, bool] = {}

        for value in self.values:
            if has_value.get(value.commodity_quantity, False):
                raise ValueError(
                    self,
                    "The measured PowerValues must contain at most one item per CommodityQuantity.",
                )

            has_value[value.commodity_quantity] = True

        return self
