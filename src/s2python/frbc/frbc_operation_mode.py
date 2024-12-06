# from itertools import pairwise
from typing import Any, Dict, List

from pydantic import root_validator

from s2python.common import NumberRange
from s2python.frbc.frbc_operation_mode_element import FRBCOperationModeElement
from s2python.generated.gen_s2 import FRBCOperationMode as GenFRBCOperationMode
from s2python.utils import pairwise
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class FRBCOperationMode(GenFRBCOperationMode, S2Message["FRBCOperationMode"]):
    class Config(GenFRBCOperationMode.Config):
        validate_assignment = True

    elements: List[FRBCOperationModeElement] = GenFRBCOperationMode.__fields__[
        "elements"
    ].field_info  # type: ignore[assignment]

    @root_validator(pre=False)
    @classmethod
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
