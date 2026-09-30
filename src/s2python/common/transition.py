import uuid
from typing import Optional, List

from s2python.common.duration import Duration
from s2python.generated.gen_s2 import Transition as GenTransition
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    S2MessageComponent,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class Transition(GenTransition, S2MessageComponent):
    model_config = copy_config(GenTransition.model_config, validate_assignment=True)

    id: uuid.UUID = copy_field(GenTransition.model_fields["id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    from_: uuid.UUID = copy_field(GenTransition.model_fields["from_"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    to: uuid.UUID = copy_field(GenTransition.model_fields["to"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    start_timers: List[uuid.UUID] = copy_field(GenTransition.model_fields["start_timers"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    blocking_timers: List[uuid.UUID] = copy_field(GenTransition.model_fields["blocking_timers"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    transition_duration: Optional[Duration] = copy_field(GenTransition.model_fields[  # type: ignore[assignment,reportIncompatibleVariableOverride]
        "transition_duration"
    ])
