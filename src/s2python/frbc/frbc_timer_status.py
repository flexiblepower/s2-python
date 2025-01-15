import uuid

from s2python.generated.gen_s2 import FRBCTimerStatus as GenFRBCTimerStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class FRBCTimerStatus(GenFRBCTimerStatus, S2Message["FRBCTimerStatus"]):
    model_config = GenFRBCTimerStatus.model_config
    model_config["validate_assignment"] = True

    actuator_id: uuid.UUID = GenFRBCTimerStatus.model_fields["actuator_id"]  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCTimerStatus.model_fields["message_id"]  # type: ignore[assignment]
    timer_id: uuid.UUID = GenFRBCTimerStatus.model_fields["timer_id"]  # type: ignore[assignment]
