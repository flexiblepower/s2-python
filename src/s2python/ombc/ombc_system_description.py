from typing import List
import uuid

from s2python.generated.gen_s2 import OMBCSystemDescription as GenOMBCSystemDescription
from s2python.ombc.ombc_operation_mode import OMBCOperationMode
from s2python.common.transition import Transition
from s2python.common.timer import Timer

from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class OMBCSystemDescription(GenOMBCSystemDescription, S2MessageComponent):
    model_config = copy_config(GenOMBCSystemDescription.model_config, validate_assignment=True)

    message_id: uuid.UUID = copy_field(GenOMBCSystemDescription.model_fields["message_id"])  # type: ignore[assignment]
    operation_modes: List[OMBCOperationMode] = copy_field(GenOMBCSystemDescription.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "operation_modes"
    ])  # type: ignore[assignment]
    transitions: List[Transition] = copy_field(GenOMBCSystemDescription.model_fields["transitions"])  # type: ignore[assignment]
    timers: List[Timer] = copy_field(GenOMBCSystemDescription.model_fields["timers"])  # type: ignore[assignment]
