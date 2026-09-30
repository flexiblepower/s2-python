from s2python.generated.gen_s2 import Duration

from s2python.generated.gen_s2 import (
    DDBCAverageDemandRateForecastElement as GenDDBCAverageDemandRateForecastElement,
)

from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class DDBCAverageDemandRateForecastElement(
    GenDDBCAverageDemandRateForecastElement,
    S2MessageComponent,
):
    model_config = copy_config(GenDDBCAverageDemandRateForecastElement.model_config, validate_assignment=True)

    duration: Duration = copy_field(GenDDBCAverageDemandRateForecastElement.model_fields["duration"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    demand_rate_expected: float = copy_field(GenDDBCAverageDemandRateForecastElement.model_fields[
        "demand_rate_expected"
    ])  # type: ignore[assignment,reportIncompatibleVariableOverride]
