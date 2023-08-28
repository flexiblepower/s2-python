from s2python.common import NumberRange
from s2python.generated.gen_s2 import FRBCStorageDescription as GenFRBCStorageDescription
from s2python.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class FRBCStorageDescription(GenFRBCStorageDescription, ValidateValuesMixin['FRBCStorageDescription']):
    class Config(GenFRBCStorageDescription.Config):
        validate_assignment = True

    fill_level_range: NumberRange = GenFRBCStorageDescription.__fields__['fill_level_range'].field_info  # type: ignore[assignment]
