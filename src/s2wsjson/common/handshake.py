from s2wsjson.generated.gen_s2 import Handshake as GenHandshake
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class Handshake(GenHandshake, ValidateValuesMixin['Handshake']):
    class Config(GenHandshake.Config):
        validate_assignment = True
