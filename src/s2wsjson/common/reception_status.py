from s2wsjson.generated.gen_s2 import ReceptionStatus as GenReceptionStatus
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class ReceptionStatus(GenReceptionStatus, ValidateValuesMixin['ReceptionStatus']):
    class Config(GenReceptionStatus.Config):
        validate_assignment = True