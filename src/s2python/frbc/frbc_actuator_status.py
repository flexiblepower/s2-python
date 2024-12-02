from pydantic import Field
from typing import Literal, Optional
import uuid

from s2python.generated.gen_s2 import FRBCActuatorStatus as GenFRBCActuatorStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class FRBCActuatorStatus(GenFRBCActuatorStatus, S2Message["FRBCActuatorStatus"]):
    class Config(GenFRBCActuatorStatus.Config):
        validate_assignment = True

    active_operation_mode_id: uuid.UUID = GenFRBCActuatorStatus.__fields__[
        "active_operation_mode_id"
    ].field_info  # type: ignore[assignment]
    actuator_id: uuid.UUID = GenFRBCActuatorStatus.__fields__["actuator_id"].field_info  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCActuatorStatus.__fields__["message_id"].field_info  # type: ignore[assignment]
    previous_operation_mode_id: Optional[uuid.UUID] = GenFRBCActuatorStatus.__fields__[
        "previous_operation_mode_id"
    ].field_info  # type: ignore[assignment]
    message_type: Literal["FRBCActuatorStatus"] = Field(default="FRBCActuatorStatus")
