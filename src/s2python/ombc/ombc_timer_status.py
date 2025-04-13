from uuid import UUID

from s2python.generated.gen_s2 import OMBCTimerStatus as GenOMBCTimerStatus

from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class OMBCTimerStatus(GenOMBCTimerStatus, S2MessageComponent):
    model_config = GenOMBCTimerStatus.model_config
    model_config["validate_assignment"] = True

    message_id: UUID = GenOMBCTimerStatus.model_fields["message_id"]  # type: ignore[assignment]
    timer_id: UUID = GenOMBCTimerStatus.model_fields["timer_id"]  # type: ignore[assignment]
