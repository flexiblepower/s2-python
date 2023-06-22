import math
import uuid
from datetime import timedelta
from typing import Optional

from s2wsjson.generated.gen_s2 import Timer as GenTimer, Duration
from s2wsjson.validate_values_mixin import ValidateValuesMixin, catch_and_convert_exceptions


def from_timedelta_to_duration(duration: timedelta) -> Duration:
    return Duration(__root__=math.ceil(duration.total_seconds() * 1000))

@catch_and_convert_exceptions
class Timer(GenTimer, ValidateValuesMixin['Timer']):
    class Config(GenTimer.Config):
        validate_assignment = True

    id: uuid.UUID = GenTimer.__fields__['id']  # type: ignore[assignment]

    def __init__(self, id: uuid.UUID, duration: 'Duration | int | timedelta', diagnostic_label: Optional[str]=None):
        if isinstance(duration, Duration):
            _duration = duration
        elif isinstance(duration, timedelta):
            _duration = from_timedelta_to_duration(duration)
        else:
            _duration = Duration(__root__=duration)

        super().__init__(id=id,
                         diagnostic_label=diagnostic_label,
                         duration=_duration)

    def duration_as_timedelta(self) -> timedelta:
        return timedelta(milliseconds=self.duration.__root__)

    def set_duration_as_timedelta(self, duration: timedelta):
        self.duration = from_timedelta_to_duration(duration)
