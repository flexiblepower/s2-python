from s2python.generated.gen_s2 import Role as GenRole
from s2python.validate_values_mixin import ValidateValuesMixin, catch_and_convert_exceptions


@catch_and_convert_exceptions
class Role(GenRole, ValidateValuesMixin['Role']):
    class Config(GenRole.Config):
        validate_assignment = True
