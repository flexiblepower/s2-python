import uuid

from s2python.generated.gen_s2 import SelectControlType as GenSelectControlType
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class SelectControlType(GenSelectControlType, S2Message["SelectControlType"]):
    model_config = GenSelectControlType.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenSelectControlType.model_fields["message_id"]  # type: ignore[assignment]
