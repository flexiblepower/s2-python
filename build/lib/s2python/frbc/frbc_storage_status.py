import uuid

from s2python.generated.gen_s2 import FRBCStorageStatus as GenFRBCStorageStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class FRBCStorageStatus(GenFRBCStorageStatus, S2Message["FRBCStorageStatus"]):
    model_config = GenFRBCStorageStatus.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenFRBCStorageStatus.model_fields["message_id"]  # type: ignore[assignment]
