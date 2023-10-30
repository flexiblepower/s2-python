import uuid

from s2python.common.duration import Duration
from s2python.generated.gen_s2 import Timer as GenTimer
from s2python.validate_values_mixin import (
    S2Message,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class Timer(GenTimer, S2Message["Timer"]):
    class Config(GenTimer.Config):
        validate_assignment = True

    id: uuid.UUID = GenTimer.__fields__["id"].field_info  # type: ignore[assignment]
    duration: Duration = GenTimer.__fields__["duration"].field_info  # type: ignore[assignment]
