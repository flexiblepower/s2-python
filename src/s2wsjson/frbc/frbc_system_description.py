from s2wsjson.generated.gen_s2 import FRBCSystemDescription as GenFRBCSystemDescription
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCSystemDescription(GenFRBCSystemDescription, ValidateValuesMixin['FRBCSystemDescription']):
    class Config(GenFRBCSystemDescription.Config):
        validate_assignment = True
