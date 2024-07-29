import uuid

from typing import List

from pydantic import model_validator

from s2python.common import Transition, Timer, Commodity
from s2python.common.support import commodity_has_quantity
from s2python.frbc.frbc_operation_mode import FRBCOperationMode
from s2python.generated.gen_s2 import (
    FRBCActuatorDescription as GenFRBCActuatorDescription,
)
from s2python.validate_values_mixin import (
    S2Message,
    catch_and_convert_exceptions,
)


@catch_and_convert_exceptions
class FRBCActuatorDescription(GenFRBCActuatorDescription, S2Message["FRBCActuatorDescription"]):
    model_config = GenFRBCActuatorDescription.model_config
    model_config["validate_assignment"] = True

    id: uuid.UUID = GenFRBCActuatorDescription.model_fields["id"]  # type: ignore[assignment]
    operation_modes: List[FRBCOperationMode] = GenFRBCActuatorDescription.model_fields[
        "operation_modes"
    ]  # type: ignore[assignment]
    transitions: List[Transition] = GenFRBCActuatorDescription.model_fields["transitions"]  # type: ignore[assignment]
    timers: List[Timer] = GenFRBCActuatorDescription.model_fields["timers"]  # type: ignore[assignment]
    supported_commodities: List[Commodity] = GenFRBCActuatorDescription.model_fields[
        "supported_commodities"
    ]  # type: ignore[assignment]

    @model_validator(mode="after")
    @classmethod
    def validate_timers_in_transitions(
        cls, frbc_actuator_description: "FRBCActuatorDescription"
    ) -> "FRBCActuatorDescription":
        timers_by_id = {timer.id: timer for timer in frbc_actuator_description.timers}
        transition: Transition
        for transition in frbc_actuator_description.transitions:
            for start_timer_id in transition.start_timers:
                if start_timer_id not in timers_by_id:
                    raise ValueError(
                        cls,
                        f"{start_timer_id} was referenced as start timer in transition "
                        f"{transition.id} but was not defined in 'timers'.",
                    )

            for blocking_timer_id in transition.blocking_timers:
                if blocking_timer_id not in timers_by_id:
                    raise ValueError(
                        cls,
                        f"{blocking_timer_id} was referenced as blocking timer in transition "
                        f"{transition.id} but was not defined in 'timers'.",
                    )

        return frbc_actuator_description

    @model_validator(mode="after")
    @classmethod
    def validate_timers_unique_ids(
        cls, frbc_actuator_description: "FRBCActuatorDescription"
    ) -> "FRBCActuatorDescription":
        ids = []
        timer: Timer
        for timer in frbc_actuator_description.timers:
            if timer.id in ids:
                raise ValueError(cls, f"Id {timer.id} was found multiple times in 'timers'.")
            ids.append(timer.id)

        return frbc_actuator_description

    @model_validator(mode="after")
    @classmethod
    def validate_operation_modes_in_transitions(
        cls, frbc_actuator_description: "FRBCActuatorDescription"
    ) -> "FRBCActuatorDescription":
        operation_mode_by_id = {
            operation_mode.id: operation_mode for operation_mode in frbc_actuator_description.operation_modes
        }
        transition: Transition
        for transition in frbc_actuator_description.transitions:
            if transition.from_ not in operation_mode_by_id:
                raise ValueError(
                    cls,
                    f"Operation mode {transition.from_} was referenced as 'from' in transition "
                    f"{transition.id} but was not defined in 'operation_modes'.",
                )

            if transition.to not in operation_mode_by_id:
                raise ValueError(
                    cls,
                    f"Operation mode {transition.to} was referenced as 'to' in transition "
                    f"{transition.id} but was not defined in 'operation_modes'.",
                )

        return frbc_actuator_description

    @model_validator(mode="after")
    @classmethod
    def validate_operation_modes_unique_ids(
        cls, frbc_actuator_description: "FRBCActuatorDescription"
    ) -> "FRBCActuatorDescription":
        ids = []
        operation_mode: FRBCOperationMode
        for operation_mode in frbc_actuator_description.operation_modes:
            if operation_mode.id in ids:
                raise ValueError(
                    cls,
                    f"Id {operation_mode.id} was found multiple times in 'operation_modes'.",
                )
            ids.append(operation_mode.id)

        return frbc_actuator_description

    @model_validator(mode="after")
    @classmethod
    def validate_operation_mode_elements_have_all_supported_commodities(
        cls, frbc_actuator_description: "FRBCActuatorDescription"
    ) -> "FRBCActuatorDescription":
        supported_commodities = frbc_actuator_description.supported_commodities
        operation_mode: FRBCOperationMode
        for operation_mode in frbc_actuator_description.operation_modes:
            for operation_mode_element in operation_mode.elements:
                for commodity in supported_commodities:
                    power_ranges_for_commodity = [
                        power_range
                        for power_range in operation_mode_element.power_ranges
                        if commodity_has_quantity(commodity, power_range.commodity_quantity)
                    ]

                    if len(power_ranges_for_commodity) > 1:
                        raise ValueError(
                            cls,
                            f"Multiple power ranges defined for commodity {commodity} in operation "
                            f"mode {operation_mode.id} and element with fill_level_range "
                            f"{operation_mode_element.fill_level_range}",
                        )
                    if not power_ranges_for_commodity:
                        raise ValueError(
                            cls,
                            f"No power ranges defined for commodity {commodity} in operation "
                            f"mode {operation_mode.id} and element with fill_level_range "
                            f"{operation_mode_element.fill_level_range}",
                        )
        return frbc_actuator_description

    @model_validator(mode="after")
    @classmethod
    def validate_unique_supported_commodities(
        cls, frbc_actuator_description: "FRBCActuatorDescription"
    ) -> "FRBCActuatorDescription":
        supported_commodities: List[Commodity] = frbc_actuator_description.supported_commodities

        for supported_commodity in supported_commodities:
            if supported_commodities.count(supported_commodity) > 1:
                raise ValueError(
                    cls,
                    f"Found duplicate {supported_commodity} commodity in 'supported_commodities'",
                )
        return frbc_actuator_description
