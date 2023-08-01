from s2wsjson.generated.gen_s2 import FRBCLeakageBehaviourElement as GenFRBCLeakageBehaviourElement
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCLeakageBehaviourElement(GenFRBCLeakageBehaviourElement, ValidateValuesMixin['FRBCLeakageBehaviourElement']):
    class Config(GenFRBCLeakageBehaviourElement.Config):
        validate_assignment = True
