from s2python.common import Duration
from s2python.generated.gen_s2 import (
    FRBCUsageForecastElement as GenFRBCUsageForecastElement,
)
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class FRBCUsageForecastElement(
    GenFRBCUsageForecastElement, S2Message["FRBCUsageForecastElement"]
):
    class Config(GenFRBCUsageForecastElement.Config):
        validate_assignment = True

    duration: Duration = GenFRBCUsageForecastElement.__fields__["duration"].field_info  # type: ignore[assignment]
