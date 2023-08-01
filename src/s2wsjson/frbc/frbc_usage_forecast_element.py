from s2wsjson.generated.gen_s2 import FRBCUsageForecastElement as GenFRBCUsageForecastElement
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCUsageForecastElement(GenFRBCUsageForecastElement, ValidateValuesMixin['FRBCUsageForecastElement']):
    class Config(GenFRBCUsageForecastElement.Config):
        validate_assignment = True

    duration: Duration = GenFRBCUsageForecastElement.__fields__['duration'].field_info  # type: ignore[assignment]
