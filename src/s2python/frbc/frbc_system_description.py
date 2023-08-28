from typing import List
import uuid

from s2python.generated.gen_s2 import FRBCSystemDescription as GenFRBCSystemDescription
from s2python.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin
from s2python.frbc import FRBCActuatorDescription, FRBCStorageDescription


@catch_and_convert_exceptions
class FRBCSystemDescription(GenFRBCSystemDescription, ValidateValuesMixin['FRBCSystemDescription']):
    class Config(GenFRBCSystemDescription.Config):
        validate_assignment = True

    actuators: List[FRBCActuatorDescription] = GenFRBCSystemDescription.__fields__['actuators'].field_info  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCSystemDescription.__fields__['message_id'].field_info  # type: ignore[assignment]
    storage: FRBCStorageDescription = GenFRBCSystemDescription.__fields__['storage'].field_info  # type: ignore[assignment]
