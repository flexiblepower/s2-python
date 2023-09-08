import json
import uuid
from datetime import timedelta
from unittest import TestCase

from s2python.common import (
    Transition,
    Duration,
    Timer,
    NumberRange,
    PowerRange,
    CommodityQuantity,
    Commodity,
)
from s2python.frbc import (
    FRBCActuatorDescription,
    FRBCOperationMode,
    FRBCOperationModeElement,
)


class FRBCActuatorDescriptionTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """{
            "diagnostic_label": "some name of actuator",
            "id": "3bdec96b-be3b-4ba9-afa0-c4a0632dded5",
            "operation_modes": [{
                "abnormal_condition_only": false,
                "diagnostic_label": "om1",
                "id": "3bdec96b-be3b-4ba9-afa0-c4a0632ffed5",
                "elements": [{ "fill_level_range": {"start_of_range": 4.0, "end_of_range": 5.0},
                               "fill_rate": {"start_of_range": 0.13, "end_of_range": 10342.569},
                               "power_ranges": [{"start_of_range": 400, "end_of_range": 6000, "commodity_quantity": "HEAT.TEMPERATURE"},
                                                {"start_of_range": 500, "end_of_range": 7000, "commodity_quantity": "ELECTRIC.POWER.L1"}],
                               "running_costs": {"start_of_range": 4.3, "end_of_range": 4.6}}]
            }],
            "supported_commodities": ["HEAT", "ELECTRICITY"],
            "timers": [{
                "diagnostic_label": "timer1",
                "duration": 2300,
                "id": "3bdec10b-be3b-4ba9-afa0-c4a0632ffed6"
            }],
            "transitions": [{ "id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3",
                              "from": "3bdec96b-be3b-4ba9-afa0-c4a0632ffed5",
                              "to": "3bdec96b-be3b-4ba9-afa0-c4a0632ffed5",
                              "start_timers": ["3bdec10b-be3b-4ba9-afa0-c4a0632ffed6"],
                              "blocking_timers": ["3bdec10b-be3b-4ba9-afa0-c4a0632ffed6"],
                              "transition_costs": 4.3,
                              "transition_duration": 1500,
                              "abnormal_condition_only": false}]
        }"""

        # Act
        frbc_actuator_description: FRBCActuatorDescription = (
            FRBCActuatorDescription.from_json(json_str)
        )

        # Assert
        expected_timer = Timer(
            id=uuid.UUID("3bdec10b-be3b-4ba9-afa0-c4a0632ffed6"),
            diagnostic_label="timer1",
            duration=Duration.from_timedelta(timedelta(seconds=2.3)),
        )

        # TODO We have to resort to using a dict as we HAVE to pass the 'from' key which is a Python reserved keyword.
        #  We will fix this by moving to pydantic v2 in which aliases have been fixed in which they may be used to
        #  assign values during init. See: https://github.com/flexiblepower/s2-ws-json-python/issues/10
        expected_transition = Transition(
            **{
                "id": uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3"),
                "from": uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632ffed5"),
                "to": uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632ffed5"),
                "start_timers": [uuid.UUID("3bdec10b-be3b-4ba9-afa0-c4a0632ffed6")],
                "blocking_timers": [uuid.UUID("3bdec10b-be3b-4ba9-afa0-c4a0632ffed6")],
                "transition_costs": 4.3,
                "transition_duration": Duration.from_milliseconds(1500),
                "abnormal_condition_only": False,
            }
        )
        expected_operation_mode_element = FRBCOperationModeElement(
            fill_level_range=NumberRange(start_of_range=4.0, end_of_range=5.0),
            fill_rate=NumberRange(start_of_range=0.13, end_of_range=10342.569),
            power_ranges=[
                PowerRange(
                    start_of_range=400,
                    end_of_range=6000,
                    commodity_quantity=CommodityQuantity.HEAT_TEMPERATURE,
                ),
                PowerRange(
                    start_of_range=500,
                    end_of_range=7000,
                    commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                ),
            ],
            running_costs=NumberRange(start_of_range=4.3, end_of_range=4.6),
        )
        expected_operation_mode = FRBCOperationMode(
            abnormal_condition_only=False,
            diagnostic_label="om1",
            id=uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632ffed5"),
            elements=[expected_operation_mode_element],
        )

        self.assertEqual(
            frbc_actuator_description.diagnostic_label, "some name of actuator"
        )
        self.assertEqual(
            frbc_actuator_description.id,
            uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632dded5"),
        )
        self.assertEqual(
            frbc_actuator_description.supported_commodities,
            [Commodity.HEAT, Commodity.ELECTRICITY],
        )
        self.assertEqual(
            frbc_actuator_description.operation_modes, [expected_operation_mode]
        )
        self.assertEqual(frbc_actuator_description.timers, [expected_timer])
        self.assertEqual(frbc_actuator_description.transitions, [expected_transition])

    def test__to_json__happy_path(self):
        # Arrange
        timer = Timer(
            id=uuid.UUID("3bdec10b-be3b-4ba9-afa0-c4a0632ffed6"),
            diagnostic_label="timer1",
            duration=Duration.from_timedelta(timedelta(seconds=2.3)),
        )

        # TODO We have to resort to using a dict as we HAVE to pass the 'from' key which is a Python reserved keyword.
        #  We will fix this by moving to pydantic v2 in which aliases have been fixed in which they may be used to
        #  assign values during init. See: https://github.com/flexiblepower/s2-ws-json-python/issues/10
        transition = Transition(
            **{
                "id": uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3"),
                "from": uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632ffed5"),
                "to": uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632ffed5"),
                "start_timers": [uuid.UUID("3bdec10b-be3b-4ba9-afa0-c4a0632ffed6")],
                "blocking_timers": [uuid.UUID("3bdec10b-be3b-4ba9-afa0-c4a0632ffed6")],
                "transition_costs": 4.3,
                "transition_duration": Duration.from_milliseconds(1500),
                "abnormal_condition_only": False,
            }
        )
        operation_mode_element = FRBCOperationModeElement(
            fill_level_range=NumberRange(start_of_range=4.0, end_of_range=5.0),
            fill_rate=NumberRange(start_of_range=0.13, end_of_range=10342.569),
            power_ranges=[
                PowerRange(
                    start_of_range=400,
                    end_of_range=6000,
                    commodity_quantity=CommodityQuantity.HEAT_TEMPERATURE,
                ),
                PowerRange(
                    start_of_range=500,
                    end_of_range=7000,
                    commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                ),
            ],
            running_costs=NumberRange(start_of_range=4.3, end_of_range=4.6),
        )
        operation_mode = FRBCOperationMode(
            abnormal_condition_only=False,
            diagnostic_label="om1",
            id=uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632ffed5"),
            elements=[operation_mode_element],
        )

        frbc_actuator_description = FRBCActuatorDescription(
            diagnostic_label="some name of actuator",
            id=uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632dded5"),
            supported_commodities=[Commodity.HEAT, Commodity.ELECTRICITY],
            operation_modes=[operation_mode],
            timers=[timer],
            transitions=[transition],
        )

        # Act
        json_str = frbc_actuator_description.to_json()

        # Assert
        expected_json = {
            "diagnostic_label": "some name of actuator",
            "id": "3bdec96b-be3b-4ba9-afa0-c4a0632dded5",
            "operation_modes": [
                {
                    "abnormal_condition_only": False,
                    "diagnostic_label": "om1",
                    "id": "3bdec96b-be3b-4ba9-afa0-c4a0632ffed5",
                    "elements": [
                        {
                            "fill_level_range": {
                                "start_of_range": 4.0,
                                "end_of_range": 5.0,
                            },
                            "fill_rate": {
                                "start_of_range": 0.13,
                                "end_of_range": 10342.569,
                            },
                            "power_ranges": [
                                {
                                    "start_of_range": 400,
                                    "end_of_range": 6000,
                                    "commodity_quantity": "HEAT.TEMPERATURE",
                                },
                                {
                                    "start_of_range": 500,
                                    "end_of_range": 7000,
                                    "commodity_quantity": "ELECTRIC.POWER.L1",
                                },
                            ],
                            "running_costs": {
                                "start_of_range": 4.3,
                                "end_of_range": 4.6,
                            },
                        }
                    ],
                }
            ],
            "supported_commodities": ["HEAT", "ELECTRICITY"],
            "timers": [
                {
                    "diagnostic_label": "timer1",
                    "duration": 2300,
                    "id": "3bdec10b-be3b-4ba9-afa0-c4a0632ffed6",
                }
            ],
            "transitions": [
                {
                    "id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3",
                    "from": "3bdec96b-be3b-4ba9-afa0-c4a0632ffed5",
                    "to": "3bdec96b-be3b-4ba9-afa0-c4a0632ffed5",
                    "start_timers": ["3bdec10b-be3b-4ba9-afa0-c4a0632ffed6"],
                    "blocking_timers": ["3bdec10b-be3b-4ba9-afa0-c4a0632ffed6"],
                    "transition_costs": 4.3,
                    "transition_duration": 1500,
                    "abnormal_condition_only": False,
                }
            ],
        }
        self.assertEqual(json.loads(json_str), expected_json)
