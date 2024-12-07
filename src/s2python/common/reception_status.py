from typing import Literal

from pydantic import Field

from s2python.generated.gen_s2 import ReceptionStatus as GenReceptionStatus
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class ReceptionStatus(GenReceptionStatus, S2Message["ReceptionStatus"]):
    class Config(GenReceptionStatus.Config):
        validate_assignment = True

    message_type: Literal["ReceptionStatus"] = Field(default="ReceptionStatus")
