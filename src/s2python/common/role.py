from s2python.generated.gen_s2 import Role as GenRole
from s2python.validate_values_mixin import (
    S2MessageComponent,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class Role(GenRole, S2MessageComponent):
    model_config = GenRole.model_config
    model_config["validate_assignment"] = True
