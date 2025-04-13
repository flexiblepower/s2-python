# from itertools import pairwise
import uuid
from typing import List, Dict
from typing_extensions import Self

from pydantic import model_validator

from s2python.common import NumberRange
from s2python.frbc.frbc_operation_mode_element import FRBCOperationModeElement
from s2python.generated.gen_s2 import FRBCOperationMode as GenFRBCOperationMode
from s2python.validate_values_mixin import (
    S2MessageComponent,
    catch_and_convert_exceptions,
)
from s2python.utils import pairwise


@catch_and_convert_exceptions
class FRBCOperationMode(GenFRBCOperationMode, S2MessageComponent):
    model_config = GenFRBCOperationMode.model_config
    model_config["validate_assignment"] = True

    id: uuid.UUID = GenFRBCOperationMode.model_fields["id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
    elements: List[FRBCOperationModeElement] = GenFRBCOperationMode.model_fields["elements"]  # type: ignore[assignment,reportIncompatibleVariableOverride]

    @model_validator(mode="after")
    def validate_contiguous_fill_levels_operation_mode_elements(self) -> Self:
        elements_by_fill_level_range: Dict[NumberRange, FRBCOperationModeElement]
        elements_by_fill_level_range = {
            element.fill_level_range: element for element in self.elements
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
                    self,
                    f"Elements with fill level ranges {current_fill_level_range} and "
                    f"{next_fill_level_range} are closest match to each other but not contiguous.",
                )
        return self
