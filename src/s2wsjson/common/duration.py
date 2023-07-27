from datetime import timedelta
import math

from s2wsjson.generated.gen_s2 import Duration as GenDuration

class Duration(GenDuration):
    def to_timedelta(self) -> timedelta:
        return timedelta(milliseconds=self.__root__)

    @staticmethod
    def from_timedelta(duration: timedelta) -> 'Duration':
        return Duration(__root__=math.ceil(duration.total_seconds() * 1000))
