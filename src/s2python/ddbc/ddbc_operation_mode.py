from typing import List
import uuid

from s2python.generated.gen_s2 import DDBCOperationMode as GenDDBCOperationMode

from s2python.common.power_range import PowerRange
from s2python.common.number_range import NumberRange

from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class DDBCOperationMode(GenDDBCOperationMode, S2Message["DDBCOperationMode"]):
    model_config = GenDDBCOperationMode.model_config
    model_config["validate_assignment"] = True

    # ? Id vs id
    id: uuid.UUID = GenDDBCOperationMode.model_fields["Id"]  # type: ignore[assignment]
    power_ranges: List[PowerRange] = GenDDBCOperationMode.model_fields["power_ranges"]  # type: ignore[assignment]
    supply_ranges: List[NumberRange] = GenDDBCOperationMode.model_fields["supply_ranges"]  # type: ignore[assignment]
    abnormal_condition_only: bool = GenDDBCOperationMode.model_fields[
        "abnormal_condition_only"
    ]  # type: ignore[assignment]
