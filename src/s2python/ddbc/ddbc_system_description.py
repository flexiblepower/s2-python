from typing import List
import uuid

from s2python.generated.gen_s2 import (
    DDBCSystemDescription as GenDDBCSystemDescription,
)
from s2python.common.number_range import NumberRange
from s2python.ddbc.ddbc_actuator_description import DDBCActuatorDescription
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class DDBCSystemDescription(GenDDBCSystemDescription, S2MessageComponent):
    model_config = GenDDBCSystemDescription.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenDDBCSystemDescription.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    actuators: List[DDBCActuatorDescription] = GenDDBCSystemDescription.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "actuators"
    ]  # type: ignore[assignment]
    present_demand_rate: NumberRange = GenDDBCSystemDescription.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "present_demand_rate"
    ]  # type: ignore[assignment]
    provides_average_demand_rate_forecast: bool = GenDDBCSystemDescription.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "provides_average_demand_rate_forecast"
    ]  # type: ignore[assignment]
