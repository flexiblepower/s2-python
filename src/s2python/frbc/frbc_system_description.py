from typing import List
import uuid

from s2python.generated.gen_s2 import FRBCSystemDescription as GenFRBCSystemDescription
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)
from s2python.frbc.frbc_actuator_description import FRBCActuatorDescription
from s2python.frbc.frbc_storage_description import FRBCStorageDescription


@catch_and_convert_exceptions
class FRBCSystemDescription(GenFRBCSystemDescription, S2MessageComponent):
    model_config = GenFRBCSystemDescription.model_config
    model_config["validate_assignment"] = True

    actuators: List[FRBCActuatorDescription] = GenFRBCSystemDescription.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "actuators"
    ]  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCSystemDescription.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    storage: FRBCStorageDescription = GenFRBCSystemDescription.model_fields["storage"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
