import uuid

from s2python.generated.gen_s2 import RevokeObject as GenRevokeObject
from s2python.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class RevokeObject(GenRevokeObject, ValidateValuesMixin['RevokeObject']):
    class Config(GenRevokeObject.Config):
        validate_assignment = True

    message_id: uuid.UUID = GenRevokeObject.__fields__['message_id'].field_info  # type: ignore[assignment]
    object_id: uuid.UUID = GenRevokeObject.__fields__['object_id'].field_info  # type: ignore[assignment]
