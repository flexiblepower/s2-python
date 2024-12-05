from pydantic import Field
from typing import Literal

from s2python.generated.gen_s2 import FRBCTimerStatus as GenFRBCTimerStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class FRBCTimerStatus(GenFRBCTimerStatus, S2Message["FRBCTimerStatus"]):
    class Config(GenFRBCTimerStatus.Config):
        validate_assignment = True

    message_type: Literal["FRBCTimerStatus"] = Field(default="FRBCTimerStatus")
