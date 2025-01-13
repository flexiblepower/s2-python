import uuid

from s2python.generated.gen_s2 import DDBCTimerStatus as GenDDBCTimerStatus

from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class DDBCTimerStatus(GenDDBCTimerStatus, S2Message["DDBCTimerStatus"]):
    model_config = GenDDBCTimerStatus.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenDDBCTimerStatus.model_fields["message_id"]  # type: ignore[assignment]
    timer_id: uuid.UUID = GenDDBCTimerStatus.model_fields["timer_id"]  # type: ignore[assignment]
    actuator_id: uuid.UUID = GenDDBCTimerStatus.model_fields["actuator_id"]  # type: ignore[assignment]
