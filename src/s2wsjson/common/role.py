from s2wsjson.generated.gen_s2 import Role as GenRole
from s2wsjson.validate_values_mixin import ValidateValuesMixin


class Role(GenRole, ValidateValuesMixin['Role']):
    class Config(GenRole.Config):
        validate_assignment = True
