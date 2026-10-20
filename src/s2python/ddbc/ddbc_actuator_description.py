from typing import List
import uuid

from s2python.generated.gen_s2 import (
    DDBCActuatorDescription as GenDDBCActuatorDescription,
)
from s2python.generated.gen_s2 import Commodity
from s2python.ddbc.ddbc_operation_mode import DDBCOperationMode

from s2python.common.timer import Timer

from s2python.validate_values_mixin import (
    copy_config,
    copy_field,
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class DDBCActuatorDescription(GenDDBCActuatorDescription, S2MessageComponent):
    model_config = copy_config(GenDDBCActuatorDescription.model_config, validate_assignment=True)

    id: uuid.UUID = copy_field(GenDDBCActuatorDescription.model_fields["id"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    supported_commodites: List[Commodity] = copy_field(GenDDBCActuatorDescription.model_fields[
        "supported_commodites"
    ])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    timers: List[Timer] = copy_field(GenDDBCActuatorDescription.model_fields["timers"])  # type: ignore[assignment,reportIncompatibleVariableOverride]
    operation_modes: List[DDBCOperationMode] = copy_field(GenDDBCActuatorDescription.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "operation_modes"
    ])  # type: ignore[assignment]
