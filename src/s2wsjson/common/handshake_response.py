from s2wsjson.generated.gen_s2 import HandshakeResponse as GenHandshakeResponse
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class HandshakeResponse(GenHandshakeResponse, ValidateValuesMixin['HandshakeResponse']):
    class Config(GenHandshakeResponse.Config):
        validate_assignment = True
