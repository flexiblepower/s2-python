import uuid
from datetime import timedelta
from typing import Optional

from s2wsjson.common.duration import Duration
from s2wsjson.generated.gen_s2 import Timer as GenTimer
from s2wsjson.validate_values_mixin import ValidateValuesMixin, catch_and_convert_exceptions


@catch_and_convert_exceptions
class Timer(GenTimer, ValidateValuesMixin['Timer']):
    class Config(GenTimer.Config):
        validate_assignment = True

    id: uuid.UUID = GenTimer.__fields__['id']  # type: ignore[assignment]
    duration: Duration = GenTimer.__fields__['duration']

    def __init__(self, id: uuid.UUID, duration: 'Duration | int | timedelta', diagnostic_label: Optional[str]=None):
        if isinstance(duration, Duration):
            _duration = duration
        elif isinstance(duration, timedelta):
            _duration = Duration.from_timedelta(duration)
        else:
            _duration = Duration(__root__=duration)

        super().__init__(id=id,
                         diagnostic_label=diagnostic_label,
                         duration=_duration)
