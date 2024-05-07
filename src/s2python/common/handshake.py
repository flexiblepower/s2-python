from s2python.generated.gen_s2 import Handshake as GenHandshake
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class Handshake(GenHandshake, S2Message["Handshake"]):
    class Config(GenHandshake.Config):
        validate_assignment = True
