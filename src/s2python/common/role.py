from s2python.generated.gen_s2 import Role as GenRole
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class Role(GenRole, S2Message["Role"]):
    class Config(GenRole.Config):
        validate_assignment = True
