import uuid

from s2python.generated.gen_s2 import SelectControlType as GenSelectControlType
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    ValidateValuesMixin,
)


@catch_and_convert_exceptions
class SelectControlType(GenSelectControlType, ValidateValuesMixin["SelectControlType"]):
    class Config(GenSelectControlType.Config):
        validate_assignment = True

    message_id: uuid.UUID = GenSelectControlType.__fields__["message_id"].field_info  # type: ignore[assignment]
