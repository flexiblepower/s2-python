from s2wsjson.generated.gen_s2 import RevokeObject as GenRevokeObject
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class RevokeObject(GenRevokeObject, ValidateValuesMixin['RevokeObject']):
    class Config(GenRevokeObject.Config):
        validate_assignment = True
