from s2python.generated.gen_s2 import Duration

from s2python.generated.gen_s2 import (
    DDBCAverageDemandRateForecastElement as GenDDBCAverageDemandRateForecastElement,
)

from s2python.validate_values_mixin import catch_and_convert_exceptions, S2MessageComponent


@catch_and_convert_exceptions
class DDBCAverageDemandRateForecastElement(
    GenDDBCAverageDemandRateForecastElement,
    S2MessageComponent,
):
    model_config = GenDDBCAverageDemandRateForecastElement.model_config
    model_config["validate_assignment"] = True

    duration: Duration = GenDDBCAverageDemandRateForecastElement.model_fields["duration"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    demand_rate_expected: float = GenDDBCAverageDemandRateForecastElement.model_fields[
        "demand_rate_expected"
    ]  # type: ignore[assignment,reportIncompatibleVariableOverride]
