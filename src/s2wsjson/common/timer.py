import uuid

from s2wsjson.common.duration import Duration
from s2wsjson.generated.gen_s2 import Timer as GenTimer
from s2wsjson.validate_values_mixin import ValidateValuesMixin, catch_and_convert_exceptions


@catch_and_convert_exceptions
class Timer(GenTimer, ValidateValuesMixin['Timer']):
    class Config(GenTimer.Config):
        validate_assignment = True

    id: uuid.UUID = GenTimer.__fields__['id'].field_info  # type: ignore[assignment]
    duration: Duration = GenTimer.__fields__['duration'].field_info  # type: ignore[assignment]
