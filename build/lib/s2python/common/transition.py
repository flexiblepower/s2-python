import uuid
from typing import Optional, List

from s2python.common.duration import Duration
from s2python.generated.gen_s2 import Transition as GenTransition
from s2python.validate_values_mixin import (
    S2Message,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class Transition(GenTransition, S2Message["Transition"]):
    model_config = GenTransition.model_config
    model_config["validate_assignment"] = True

    id: uuid.UUID = GenTransition.model_fields["id"]  # type: ignore[assignment]
    from_: uuid.UUID = GenTransition.model_fields["from_"]  # type: ignore[assignment]
    to: uuid.UUID = GenTransition.model_fields["to"]  # type: ignore[assignment]
    start_timers: List[uuid.UUID] = GenTransition.model_fields["start_timers"]  # type: ignore[assignment]
    blocking_timers: List[uuid.UUID] = GenTransition.model_fields["blocking_timers"]  # type: ignore[assignment]
    transition_duration: Optional[Duration] = GenTransition.model_fields[
        "transition_duration"
    ]  # type: ignore[assignment]
