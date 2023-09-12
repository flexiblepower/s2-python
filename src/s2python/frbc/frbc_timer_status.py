import uuid

from s2python.generated.gen_s2 import FRBCTimerStatus as GenFRBCTimerStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    ValidateValuesMixin,
)


@catch_and_convert_exceptions
class FRBCTimerStatus(GenFRBCTimerStatus, ValidateValuesMixin["FRBCTimerStatus"]):
    class Config(GenFRBCTimerStatus.Config):
        validate_assignment = True

    actuator_id: uuid.UUID = GenFRBCTimerStatus.__fields__["actuator_id"].field_info  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCTimerStatus.__fields__["message_id"].field_info  # type: ignore[assignment]
    timer_id: uuid.UUID = GenFRBCTimerStatus.__fields__["timer_id"].field_info  # type: ignore[assignment]
