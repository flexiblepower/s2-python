from s2wsjson.generated.gen_s2 import Transition as GenTransition
from s2wsjson.validate_values_mixin import ValidateValuesMixin


class Transition(GenTransition, ValidateValuesMixin['Transition']):
    class Config(GenTransition.Config):
        validate_assignment = True
