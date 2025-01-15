from s2python.common import NumberRange
from s2python.generated.gen_s2 import (
    FRBCStorageDescription as GenFRBCStorageDescription,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class FRBCStorageDescription(GenFRBCStorageDescription, S2Message["FRBCStorageDescription"]):
    model_config = GenFRBCStorageDescription.model_config
    model_config["validate_assignment"] = True

    fill_level_range: NumberRange = GenFRBCStorageDescription.model_fields[
        "fill_level_range"
    ]  # type: ignore[assignment]
