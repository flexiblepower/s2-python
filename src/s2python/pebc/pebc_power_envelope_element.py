from s2python.generated.gen_s2 import (
    PEBCPowerEnvelopeElement as GenPEBCPowerEnvelopeElement,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PEBCPowerEnvelopeElement(
    GenPEBCPowerEnvelopeElement, S2Message["PEBCPowerEnvelopeElement"]
):
    model_config = GenPEBCPowerEnvelopeElement.model_config
    model_config["validate_assignment"] = True

    lower_limit: float = GenPEBCPowerEnvelopeElement.model_fields["lower_limit"]  # type: ignore[assignment]
    upper_limit: float = GenPEBCPowerEnvelopeElement.model_fields["upper_limit"]  # type: ignore[assignment]
