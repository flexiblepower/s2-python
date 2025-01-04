from typing import List
from s2python.generated.gen_s2 import (
    PEBCPowerEnvelope as GenPEBCPowerEnvelope,
)
from s2python.pebc.pebc_power_envelope_element import PEBCPowerEnvelopeElement
from s2python.common import CommodityQuantity
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PEBCPowerEnvelope(GenPEBCPowerEnvelope, S2Message["PEBCPowerEnvelope"]):
    model_config = GenPEBCPowerEnvelope.model_config
    model_config["validate_assignment"] = True

    commodity_quantity: CommodityQuantity = GenPEBCPowerEnvelope.model_fields[
        "commodity_quantity"
    ]  # type: ignore[assignment]
    power_envelope_elements: List[PEBCPowerEnvelopeElement] = GenPEBCPowerEnvelope.model_fields[
        "power_envelope_elements"
    ]  # type: ignore[assignment]
