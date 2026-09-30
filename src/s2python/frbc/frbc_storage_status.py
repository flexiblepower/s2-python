import uuid

from s2python.generated.gen_s2 import FRBCStorageStatus as GenFRBCStorageStatus
from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class FRBCStorageStatus(GenFRBCStorageStatus, S2MessageComponent):
    model_config = copy_config(GenFRBCStorageStatus.model_config, validate_assignment=True)

    message_id: uuid.UUID = copy_field(GenFRBCStorageStatus.model_fields["message_id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
