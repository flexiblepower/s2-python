from s2wsjson.generated.gen_s2 import Role as GenRole
from s2wsjson.validate_values_mixin import ValidateValuesMixin, catch_and_convert_exceptions


@catch_and_convert_exceptions
class Role(GenRole, ValidateValuesMixin['Role']):
    class Config(GenRole.Config):
        validate_assignment = True
