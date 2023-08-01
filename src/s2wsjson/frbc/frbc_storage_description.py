from s2wsjson.generated.gen_s2 import FRBCStorageDescription as GenFRBCStorageDescription
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCStorageDescription(GenFRBCStorageDescription, ValidateValuesMixin['FRBCStorageDescription']):
    class Config(GenFRBCStorageDescription.Config):
        validate_assignment = True
