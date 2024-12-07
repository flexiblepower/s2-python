from typing import Literal

from pydantic import Field

from s2python.generated.gen_s2 import FRBCStorageStatus as GenFRBCStorageStatus
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class FRBCStorageStatus(GenFRBCStorageStatus, S2Message["FRBCStorageStatus"]):
    class Config(GenFRBCStorageStatus.Config):
        validate_assignment = True

    message_type: Literal["FRBC.StorageStatus"] = Field(default="FRBC.StorageStatus")
