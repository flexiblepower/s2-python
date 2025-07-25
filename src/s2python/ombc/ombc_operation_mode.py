from typing import List
import uuid

from s2python.generated.gen_s2 import OMBCOperationMode as GenOMBCOperationMode
from s2python.common.power_range import PowerRange


from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class OMBCOperationMode(GenOMBCOperationMode, S2MessageComponent):
    model_config = GenOMBCOperationMode.model_config
    model_config["validate_assignment"] = True

    id: uuid.UUID = GenOMBCOperationMode.model_fields["id"]  # type: ignore[assignment]
    power_ranges: List[PowerRange] = GenOMBCOperationMode.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "power_ranges"
    ]  # type: ignore[assignment]
    abnormal_condition_only: bool = GenOMBCOperationMode.model_fields[
        "abnormal_condition_only"
    ]  # type: ignore[assignment]
