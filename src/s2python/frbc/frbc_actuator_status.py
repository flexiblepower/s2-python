from typing import Literal

from pydantic import Field

from s2python.generated.gen_s2 import FRBCActuatorStatus as GenFRBCActuatorStatus
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class FRBCActuatorStatus(GenFRBCActuatorStatus, S2Message["FRBCActuatorStatus"]):
    class Config(GenFRBCActuatorStatus.Config):
        validate_assignment = True

    message_type: Literal["FRBC.ActuatorStatus"] = Field(default="FRBC.ActuatorStatus")
