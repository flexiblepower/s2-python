import uuid

from s2python.generated.gen_s2 import (
    PEBCEnergyConstraint as GenPEBCEnergyConstraint,
)
from s2python.common import CommodityQuantity
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PEBCEnergyConstraint(GenPEBCEnergyConstraint, S2Message["PEBCEnergyConstraint"]):
    model_config = GenPEBCEnergyConstraint.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenPEBCEnergyConstraint.model_fields["message_id"]  # type: ignore[assignment]
    id: uuid.UUID = GenPEBCEnergyConstraint.model_fields["id"]  # type: ignore[assignment]

    upper_average_power: float = GenPEBCEnergyConstraint.model_fields["upper_average_power"]  # type: ignore[assignment]
    lower_average_power: float = GenPEBCEnergyConstraint.model_fields["lower_average_power"]  # type: ignore[assignment]
    commodity_quantity: CommodityQuantity = GenPEBCEnergyConstraint.model_fields["commodity_quantity"]  # type: ignore[assignment]
