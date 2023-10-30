import uuid

from s2python.generated.gen_s2 import ReceptionStatus as GenReceptionStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class ReceptionStatus(GenReceptionStatus, S2Message["ReceptionStatus"]):
    class Config(GenReceptionStatus.Config):
        validate_assignment = True

    subject_message_id: uuid.UUID = GenReceptionStatus.__fields__[
        "subject_message_id"
    ].field_info  # type: ignore[assignment]
