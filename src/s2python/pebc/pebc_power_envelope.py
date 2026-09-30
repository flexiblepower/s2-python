from typing import List
from s2python.generated.gen_s2 import (
    PEBCPowerEnvelope as GenPEBCPowerEnvelope,
)
from s2python.pebc.pebc_power_envelope_element import PEBCPowerEnvelopeElement
from s2python.common import CommodityQuantity
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class PEBCPowerEnvelope(GenPEBCPowerEnvelope, S2MessageComponent):
    model_config = copy_config(GenPEBCPowerEnvelope.model_config, validate_assignment=True)

    commodity_quantity: CommodityQuantity = copy_field(GenPEBCPowerEnvelope.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "commodity_quantity"
    ])  # type: ignore[assignment]
    power_envelope_elements: List[PEBCPowerEnvelopeElement] = copy_field(GenPEBCPowerEnvelope.model_fields[  # type: ignore[assignment,reportIncompatibleVariableOverride]
        "power_envelope_elements"
    ])  # type: ignore[assignment]
