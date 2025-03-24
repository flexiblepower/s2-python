from typing import List

from s2python.generated.gen_s2 import (
    PPBCPowerSequenceElement as GenPPBCPowerSequenceElement,
)

from s2python.validate_values_mixin import (
    S2MessageComponent,
    catch_and_convert_exceptions,
)

from s2python.common import Duration, PowerForecastValue


@catch_and_convert_exceptions
class PPBCPowerSequenceElement(GenPPBCPowerSequenceElement, S2MessageComponent):
    model_config = GenPPBCPowerSequenceElement.model_config
    model_config["validate_assignment"] = True

    duration: Duration = GenPPBCPowerSequenceElement.model_fields["duration"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    power_values: List[PowerForecastValue] = GenPPBCPowerSequenceElement.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "power_values"
    ]  # type: ignore[assignment]
