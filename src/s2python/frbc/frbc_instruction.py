import uuid

from s2python.generated.gen_s2 import FRBCInstruction as GenFRBCInstruction
from s2python.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCInstruction(GenFRBCInstruction, ValidateValuesMixin['FRBCInstruction']):
    class Config(GenFRBCInstruction.Config):
        validate_assignment = True

    actuator_id: uuid.UUID = GenFRBCInstruction.__fields__['actuator_id'].field_info  # type: ignore[assignment]
    id: uuid.UUID = GenFRBCInstruction.__fields__['id'].field_info  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCInstruction.__fields__['message_id'].field_info  # type: ignore[assignment]
    operation_mode:  uuid.UUID = GenFRBCInstruction.__fields__['operation_mode'].field_info  # type: ignore[assignment]
