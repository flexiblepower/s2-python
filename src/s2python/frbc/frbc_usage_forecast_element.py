from s2python.common import Duration

from s2python.generated.gen_s2 import (
    FRBCUsageForecastElement as GenFRBCUsageForecastElement,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class FRBCUsageForecastElement(GenFRBCUsageForecastElement, S2MessageComponent):
    model_config = GenFRBCUsageForecastElement.model_config
    model_config["validate_assignment"] = True

    duration: Duration = GenFRBCUsageForecastElement.model_fields["duration"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
