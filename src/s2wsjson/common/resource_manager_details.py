from s2wsjson.generated.gen_s2 import ResourceManagerDetails as GenResourceManagerDetails
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class ResourceManagerDetails(GenResourceManagerDetails, ValidateValuesMixin['ResourceManagerDetails']):
    class Config(GenResourceManagerDetails.Config):
        validate_assignment = True
