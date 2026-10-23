import uuid

from s2python.generated.gen_s2 import (
    PEBCEnergyConstraint as GenPEBCEnergyConstraint,
)
from s2python.common import CommodityQuantity
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class PEBCEnergyConstraint(GenPEBCEnergyConstraint, S2MessageComponent):
    model_config = copy_config(GenPEBCEnergyConstraint.model_config, validate_assignment=True)

    message_id: uuid.UUID = copy_field(GenPEBCEnergyConstraint.model_fields["message_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    id: uuid.UUID = copy_field(GenPEBCEnergyConstraint.model_fields["id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]

    upper_average_power: float = copy_field(GenPEBCEnergyConstraint.model_fields["upper_average_power"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    lower_average_power: float = copy_field(GenPEBCEnergyConstraint.model_fields["lower_average_power"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    commodity_quantity: CommodityQuantity = [
        copy_field(GenPEBCEnergyConstraint.model_fields["commodity_quantity"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    ]
