from s2wsjson.generated.gen_s2 import FRBCOperationModeElement as GenFRBCOperationModeElement
from s2wsjson.validate_values_mixin import ValidateValuesMixin, catch_and_convert_exceptions


@catch_and_convert_exceptions
class FRBCOperationModeElement(GenFRBCOperationModeElement, ValidateValuesMixin['FRBCOperationModeElement']):
    class Config(GenFRBCOperationModeElement.Config):
        validate_assignment = True
