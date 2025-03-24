import uuid

from s2python.generated.gen_s2 import (
    PEBCEnergyConstraint as GenPEBCEnergyConstraint,
)
from s2python.common import CommodityQuantity
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class PEBCEnergyConstraint(GenPEBCEnergyConstraint, S2MessageComponent):
    model_config = GenPEBCEnergyConstraint.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenPEBCEnergyConstraint.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    id: uuid.UUID = GenPEBCEnergyConstraint.model_fields["id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]

    upper_average_power: float = GenPEBCEnergyConstraint.model_fields["upper_average_power"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    lower_average_power: float = GenPEBCEnergyConstraint.model_fields["lower_average_power"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    commodity_quantity: CommodityQuantity = [
        GenPEBCEnergyConstraint.model_fields["commodity_quantity"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    ]
