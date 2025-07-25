from typing import List
import uuid

from s2python.generated.gen_s2 import OMBCSystemDescription as GenOMBCSystemDescription
from s2python.ombc.ombc_operation_mode import OMBCOperationMode
from s2python.common.transition import Transition
from s2python.common.timer import Timer

from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class OMBCSystemDescription(GenOMBCSystemDescription, S2MessageComponent):
    model_config = GenOMBCSystemDescription.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenOMBCSystemDescription.model_fields["message_id"]  # type: ignore[assignment]
    operation_modes: List[OMBCOperationMode] = GenOMBCSystemDescription.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "operation_modes"
    ]  # type: ignore[assignment]
    transitions: List[Transition] = GenOMBCSystemDescription.model_fields["transitions"]  # type: ignore[assignment]
    timers: List[Timer] = GenOMBCSystemDescription.model_fields["timers"]  # type: ignore[assignment]
