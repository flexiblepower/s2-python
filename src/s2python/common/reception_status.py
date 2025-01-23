import uuid

from s2python.generated.gen_s2 import ReceptionStatus as GenReceptionStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class ReceptionStatus(GenReceptionStatus, S2MessageComponent["ReceptionStatus"]):
    model_config = GenReceptionStatus.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenReceptionStatus.model_fields["message_id"]  # type: ignore[assignment]
