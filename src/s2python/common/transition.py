import uuid
from typing import Optional, List

from s2python.common import Duration
from s2python.generated.gen_s2 import Transition as GenTransition
from s2python.validate_values_mixin import ValidateValuesMixin, catch_and_convert_exceptions


@catch_and_convert_exceptions
class Transition(GenTransition, ValidateValuesMixin['Transition']):
    class Config(GenTransition.Config):
        validate_assignment = True

    id: uuid.UUID = GenTransition.__fields__['id'].field_info  # type: ignore[assignment]
    from_: uuid.UUID = GenTransition.__fields__['from_'].field_info  # type: ignore[assignment]
    to: uuid.UUID = GenTransition.__fields__['to'].field_info  # type: ignore[assignment]
    start_timers: List[uuid.UUID] = GenTransition.__fields__['start_timers'].field_info  # type: ignore[assignment]
    blocking_timers: List[uuid.UUID] = GenTransition.__fields__['blocking_timers'].field_info  # type: ignore[assignment]
    transition_duration: Optional[Duration] = GenTransition.__fields__['transition_duration'].field_info  # type: ignore[assignment]
