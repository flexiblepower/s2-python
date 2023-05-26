from s2wsjson.generated.gen_s2 import FRBCOperationModeElement as GenFRBCOperationModeElement
from s2wsjson.validate_values_mixin import ValidateValuesMixin


class FRBCOperationModeElement(GenFRBCOperationModeElement, ValidateValuesMixin['FRBCOperationModeElement']):
    class Config(GenFRBCOperationModeElement.Config):
        validate_assignment = True
