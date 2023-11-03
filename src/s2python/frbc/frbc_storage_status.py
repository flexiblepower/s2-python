import uuid

from s2python.generated.gen_s2 import FRBCStorageStatus as GenFRBCStorageStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class FRBCStorageStatus(GenFRBCStorageStatus, S2Message["FRBCStorageStatus"]):
    class Config(GenFRBCStorageStatus.Config):
        validate_assignment = True

    message_id: uuid.UUID = GenFRBCStorageStatus.__fields__["message_id"].field_info  # type: ignore[assignment]
