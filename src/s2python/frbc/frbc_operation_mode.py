# from itertools import pairwise
import uuid
from typing import List, Dict, Any, Generator, Tuple

from pydantic import root_validator

from s2python.common import NumberRange
from s2python.frbc import FRBCOperationModeElement
from s2python.generated.gen_s2 import FRBCOperationMode as GenFRBCOperationMode
from s2python.validate_values_mixin import (
    ValidateValuesMixin,
    catch_and_convert_exceptions,
)
from s2python.utils import pairwise


@catch_and_convert_exceptions
class FRBCOperationMode(GenFRBCOperationMode, ValidateValuesMixin["FRBCOperationMode"]):
    class Config(GenFRBCOperationMode.Config):
        validate_assignment = True

    id: uuid.UUID = GenFRBCOperationMode.__fields__["id"].field_info  # type: ignore[assignment]
    elements: List[FRBCOperationModeElement] = GenFRBCOperationMode.__fields__[
        "elements"
    ].field_info  # type: ignore[assignment]

    @root_validator(pre=False)
    def validate_contiguous_fill_levels_operation_mode_elements(
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        elements_by_fill_level_range: Dict[NumberRange, FRBCOperationModeElement]
        elements_by_fill_level_range = {
            element.fill_level_range: element for element in values.get("elements", [])
        }

        sorted_fill_level_ranges: List[NumberRange]
        sorted_fill_level_ranges = list(elements_by_fill_level_range.keys())
        sorted_fill_level_ranges.sort(key=lambda r: r.start_of_range)

        for current_fill_level_range, next_fill_level_range in pairwise(
            sorted_fill_level_ranges
        ):
            if (
                current_fill_level_range.end_of_range
                != next_fill_level_range.start_of_range
            ):
                raise ValueError(
                    cls,
                    f"Elements with fill level ranges {current_fill_level_range} and "
                    f"{next_fill_level_range} are closest match to each other but not contiguous.",
                )
        return values
