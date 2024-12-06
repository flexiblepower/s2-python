from typing import Optional

from s2python.common.duration import Duration
from s2python.generated.gen_s2 import Transition as GenTransition
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class Transition(GenTransition, S2Message["Transition"]):
    class Config(GenTransition.Config):
        validate_assignment = True

    transition_duration: Optional[Duration] = GenTransition.__fields__[
        "transition_duration"
    ].field_info  # type: ignore[assignment]
