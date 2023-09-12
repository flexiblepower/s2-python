from datetime import timedelta
import math

from s2python.generated.gen_s2 import Duration as GenDuration
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    ValidateValuesMixin,
)


@catch_and_convert_exceptions
class Duration(GenDuration, ValidateValuesMixin["Duration"]):
    def to_timedelta(self) -> timedelta:
        return timedelta(milliseconds=self.__root__)

    @staticmethod
    def from_timedelta(duration: timedelta) -> "Duration":
        return Duration(__root__=math.ceil(duration.total_seconds() * 1000))

    @staticmethod
    def from_milliseconds(milliseconds: int) -> "Duration":
        return Duration(__root__=milliseconds)
