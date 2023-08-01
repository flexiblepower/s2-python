from s2wsjson.generated.gen_s2 import FRBCStorageStatus as GenFRBCStorageStatus
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCStorageStatus(GenFRBCStorageStatus, ValidateValuesMixin['FRBCStorageStatus']):
    class Config(GenFRBCStorageStatus.Config):
        validate_assignment = True
