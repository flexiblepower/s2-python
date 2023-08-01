from s2wsjson.generated.gen_s2 import FRBCFillLevelTargetProfile as GenFRBCFillLevelTargetProfile
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCFillLevelTargetProfile(GenFRBCFillLevelTargetProfile, ValidateValuesMixin['FRBCFillLevelTargetProfile']):
    class Config(GenFRBCFillLevelTargetProfile.Config):
        validate_assignment = True
