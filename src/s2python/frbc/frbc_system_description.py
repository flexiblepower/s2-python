from typing import List
import uuid

from s2python.generated.gen_s2 import FRBCSystemDescription as GenFRBCSystemDescription
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)
from s2python.frbc.frbc_actuator_description import FRBCActuatorDescription
from s2python.frbc.frbc_storage_description import FRBCStorageDescription


@catch_and_convert_exceptions
class FRBCSystemDescription(GenFRBCSystemDescription, S2MessageComponent):
    model_config = copy_config(GenFRBCSystemDescription.model_config, validate_assignment=True)

    actuators: List[FRBCActuatorDescription] = copy_field(GenFRBCSystemDescription.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "actuators"
    ])  # type: ignore[assignment]
    message_id: uuid.UUID = copy_field(GenFRBCSystemDescription.model_fields["message_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    storage: FRBCStorageDescription = copy_field(GenFRBCSystemDescription.model_fields["storage"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
