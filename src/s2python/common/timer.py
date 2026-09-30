import uuid

from s2python.common.duration import Duration
from s2python.generated.gen_s2 import Timer as GenTimer
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    S2MessageComponent,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class Timer(GenTimer, S2MessageComponent):
    model_config = copy_config(GenTimer.model_config, validate_assignment=True)

    id: uuid.UUID = copy_field(GenTimer.model_fields["id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    duration: Duration = copy_field(GenTimer.model_fields["duration"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
