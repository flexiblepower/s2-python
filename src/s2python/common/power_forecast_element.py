from typing import List, Dict
from typing_extensions import Self

from pydantic import model_validator

from s2python.generated.gen_s2 import (
    CommodityQuantity,
    PowerForecastElement as GenPowerForecastElement,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)
from s2python.common.duration import Duration
from s2python.common.power_forecast_value import PowerForecastValue


@catch_and_convert_exceptions
class PowerForecastElement(GenPowerForecastElement, S2MessageComponent):
    model_config = GenPowerForecastElement.model_config
    model_config["validate_assignment"] = True

    duration: Duration = GenPowerForecastElement.model_fields["duration"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    power_values: List[PowerForecastValue] = (  # type: ignore[reportIncompatibleVariableOverride]
        GenPowerForecastElement.model_fields["power_values"]  # type: ignore[assignment]
    )

    @model_validator(mode="after")
    def validate_values_at_most_one_per_commodity_quantity(self) -> Self:
        """Validates the power measurement values to check that there is at most 1 PowerValue per CommodityQuantity."""

        has_value: Dict[CommodityQuantity, bool] = {}

        for value in self.power_values:
            if has_value.get(value.commodity_quantity, False):
                raise ValueError(
                    self,
                    "There must be at most 1 PowerForecastValue per CommodityQuantity",
                )
            has_value[value.commodity_quantity] = True

        return self
