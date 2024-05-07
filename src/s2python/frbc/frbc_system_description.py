from pydantic import Field
from typing import List, Literal

from s2python.generated.gen_s2 import FRBCSystemDescription as GenFRBCSystemDescription
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)
from s2python.frbc.frbc_actuator_description import FRBCActuatorDescription
from s2python.frbc.frbc_storage_description import FRBCStorageDescription


@catch_and_convert_exceptions
class FRBCSystemDescription(
    GenFRBCSystemDescription, S2Message["FRBCSystemDescription"]
):
    class Config(GenFRBCSystemDescription.Config):
        validate_assignment = True

    actuators: List[FRBCActuatorDescription] = GenFRBCSystemDescription.__fields__[
        "actuators"
    ].field_info  # type: ignore[assignment]
    storage: FRBCStorageDescription = GenFRBCSystemDescription.__fields__[
        "storage"
    ].field_info  # type: ignore[assignment]
    message_type: Literal["FRBCSystemDescription"] = Field(default="FRBCSystemDescription")
