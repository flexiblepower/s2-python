from s2wsjson.generated.gen_s2 import FRBCLeakageBehaviour as GenFRBCLeakageBehaviour
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCLeakageBehaviour(GenFRBCLeakageBehaviour, ValidateValuesMixin['FRBCLeakageBehaviour']):
    class Config(GenFRBCLeakageBehaviour.Config):
        validate_assignment = True
