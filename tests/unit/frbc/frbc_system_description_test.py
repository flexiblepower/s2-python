from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCSystemDescriptionTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "actuators": [
        {
            "diagnostic_label": "some-test-string2728",
            "id": "a1061148-f19e-4b1b-8fe3-b506583ce61e",
            "operation_modes": [
                {
                    "abnormal_condition_only": false,
                    "diagnostic_label": "some-test-string2930",
                    "elements": [
                        {
                            "fill_level_range": {
                                "end_of_range": 36932.65171036228,
                                "start_of_range": 12649.272766336762
                            },
                            "fill_rate": {
                                "end_of_range": 34553.16163528188,
                                "start_of_range": 14377.963894945604
                            },
                            "power_ranges": [
                                {
                                    "commodity_quantity": "ELECTRIC.POWER.L1",
                                    "end_of_range": 46924.65023353163,
                                    "start_of_range": 11888.235871902496
                                }
                            ],
                            "running_costs": {
                                "end_of_range": 42897.60731684277,
                                "start_of_range": 33997.56376994998
                            }
                        }
                    ],
                    "id": "2795136c-eb30-4f8a-bdaa-61feba1e71b6"
                }
            ],
            "supported_commodities": [
                "ELECTRICITY"
            ],
            "timers": [
                {
                    "diagnostic_label": "some-test-string4315",
                    "duration": 14099,
                    "id": "e1ff9e58-935b-4765-92e3-5e7679f73eb6"
                }
            ],
            "transitions": [
                {
                    "abnormal_condition_only": true,
                    "blocking_timers": [
                        "e1ff9e58-935b-4765-92e3-5e7679f73eb6"
                    ],
                    "from": "2795136c-eb30-4f8a-bdaa-61feba1e71b6",
                    "id": "c32cc1d3-4722-41e3-a8de-55307c723611",
                    "start_timers": [
                        "e1ff9e58-935b-4765-92e3-5e7679f73eb6"
                    ],
                    "to": "2795136c-eb30-4f8a-bdaa-61feba1e71b6",
                    "transition_costs": 1018.4228054114793,
                    "transition_duration": 11988
                }
            ]
        }
    ],
    "message_id": "97256813-de70-4640-a992-9ae0b2d8e4d1",
    "message_type": "FRBC.SystemDescription",
    "storage": {
        "diagnostic_label": "some-test-string8418",
        "fill_level_label": "some-test-string9512",
        "fill_level_range": {
            "end_of_range": 20876.752745956997,
            "start_of_range": 18324.0229135081
        },
        "provides_fill_level_target_profile": false,
        "provides_leakage_behaviour": true,
        "provides_usage_forecast": false
    },
    "valid_from": "2020-10-07T06:30:55Z"
}
        """

        # Act
        frbc_system_description = FRBCSystemDescription.from_json(json_str)

        # Assert
        # TODO We have to resort to using a dict as we HAVE to pass the 'from' key which is a Python reserved keyword.
        #  We will fix this by moving to pydantic v2 in which aliases have been fixed in which they may be used to
        #  assign values during init. See: https://github.com/flexiblepower/s2-ws-json-python/issues/10
        transition = Transition(
            **{
                "id": uuid.UUID("c32cc1d3-4722-41e3-a8de-55307c723611"),
                "from": uuid.UUID("2795136c-eb30-4f8a-bdaa-61feba1e71b6"),
                "to": uuid.UUID("2795136c-eb30-4f8a-bdaa-61feba1e71b6"),
                "start_timers": [uuid.UUID("e1ff9e58-935b-4765-92e3-5e7679f73eb6")],
                "blocking_timers": [uuid.UUID("e1ff9e58-935b-4765-92e3-5e7679f73eb6")],
                "transition_costs": 1018.4228054114793,
                "transition_duration": Duration.from_milliseconds(11988),
                "abnormal_condition_only": True,
            }
        )

        self.assertEqual(
            frbc_system_description.actuators,
            [
                FRBCActuatorDescription(
                    diagnostic_label="some-test-string2728",
                    id=uuid.UUID("a1061148-f19e-4b1b-8fe3-b506583ce61e"),
                    operation_modes=[
                        FRBCOperationMode(
                            abnormal_condition_only=False,
                            diagnostic_label="some-test-string2930",
                            elements=[
                                FRBCOperationModeElement(
                                    fill_level_range=NumberRange(
                                        end_of_range=36932.65171036228,
                                        start_of_range=12649.272766336762,
                                    ),
                                    fill_rate=NumberRange(
                                        end_of_range=34553.16163528188,
                                        start_of_range=14377.963894945604,
                                    ),
                                    power_ranges=[
                                        PowerRange(
                                            commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                                            end_of_range=46924.65023353163,
                                            start_of_range=11888.235871902496,
                                        )
                                    ],
                                    running_costs=NumberRange(
                                        end_of_range=42897.60731684277,
                                        start_of_range=33997.56376994998,
                                    ),
                                )
                            ],
                            id=uuid.UUID("2795136c-eb30-4f8a-bdaa-61feba1e71b6"),
                        )
                    ],
                    supported_commodities=[Commodity.ELECTRICITY],
                    timers=[
                        Timer(
                            diagnostic_label="some-test-string4315",
                            duration=Duration.from_timedelta(
                                timedelta(milliseconds=14099)
                            ),
                            id=uuid.UUID("e1ff9e58-935b-4765-92e3-5e7679f73eb6"),
                        )
                    ],
                    transitions=[transition],
                )
            ],
        )
        self.assertEqual(
            frbc_system_description.message_id,
            uuid.UUID("97256813-de70-4640-a992-9ae0b2d8e4d1"),
        )
        self.assertEqual(frbc_system_description.message_type, "FRBC.SystemDescription")
        self.assertEqual(
            frbc_system_description.storage,
            FRBCStorageDescription(
                diagnostic_label="some-test-string8418",
                fill_level_label="some-test-string9512",
                fill_level_range=NumberRange(
                    end_of_range=20876.752745956997, start_of_range=18324.0229135081
                ),
                provides_fill_level_target_profile=False,
                provides_leakage_behaviour=True,
                provides_usage_forecast=False,
            ),
        )
        self.assertEqual(
            frbc_system_description.valid_from,
            datetime(
                year=2020,
                month=10,
                day=7,
                hour=6,
                minute=30,
                second=55,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
        )

    def test__to_json__happy_path_full(self):
        # Arrange
        # TODO We have to resort to using a dict as we HAVE to pass the 'from' key which is a Python reserved keyword.
        #  We will fix this by moving to pydantic v2 in which aliases have been fixed in which they may be used to
        #  assign values during init. See: https://github.com/flexiblepower/s2-ws-json-python/issues/10
        transition = Transition(
            **{
                "id": uuid.UUID("c32cc1d3-4722-41e3-a8de-55307c723611"),
                "from": uuid.UUID("2795136c-eb30-4f8a-bdaa-61feba1e71b6"),
                "to": uuid.UUID("2795136c-eb30-4f8a-bdaa-61feba1e71b6"),
                "start_timers": [uuid.UUID("e1ff9e58-935b-4765-92e3-5e7679f73eb6")],
                "blocking_timers": [uuid.UUID("e1ff9e58-935b-4765-92e3-5e7679f73eb6")],
                "transition_costs": 1018.4228054114793,
                "transition_duration": Duration.from_milliseconds(11988),
                "abnormal_condition_only": True,
            }
        )
        frbc_system_description = FRBCSystemDescription(
            actuators=[
                FRBCActuatorDescription(
                    diagnostic_label="some-test-string2728",
                    id=uuid.UUID("a1061148-f19e-4b1b-8fe3-b506583ce61e"),
                    operation_modes=[
                        FRBCOperationMode(
                            abnormal_condition_only=False,
                            diagnostic_label="some-test-string2930",
                            elements=[
                                FRBCOperationModeElement(
                                    fill_level_range=NumberRange(
                                        end_of_range=36932.65171036228,
                                        start_of_range=12649.272766336762,
                                    ),
                                    fill_rate=NumberRange(
                                        end_of_range=34553.16163528188,
                                        start_of_range=14377.963894945604,
                                    ),
                                    power_ranges=[
                                        PowerRange(
                                            commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                                            end_of_range=46924.65023353163,
                                            start_of_range=11888.235871902496,
                                        )
                                    ],
                                    running_costs=NumberRange(
                                        end_of_range=42897.60731684277,
                                        start_of_range=33997.56376994998,
                                    ),
                                )
                            ],
                            id=uuid.UUID("2795136c-eb30-4f8a-bdaa-61feba1e71b6"),
                        )
                    ],
                    supported_commodities=[Commodity.ELECTRICITY],
                    timers=[
                        Timer(
                            diagnostic_label="some-test-string4315",
                            duration=Duration.from_timedelta(
                                timedelta(milliseconds=14099)
                            ),
                            id=uuid.UUID("e1ff9e58-935b-4765-92e3-5e7679f73eb6"),
                        )
                    ],
                    transitions=[transition],
                )
            ],
            message_id=uuid.UUID("97256813-de70-4640-a992-9ae0b2d8e4d1"),
            message_type="FRBC.SystemDescription",
            storage=FRBCStorageDescription(
                diagnostic_label="some-test-string8418",
                fill_level_label="some-test-string9512",
                fill_level_range=NumberRange(
                    end_of_range=20876.752745956997, start_of_range=18324.0229135081
                ),
                provides_fill_level_target_profile=False,
                provides_leakage_behaviour=True,
                provides_usage_forecast=False,
            ),
            valid_from=datetime(
                year=2020,
                month=10,
                day=7,
                hour=6,
                minute=30,
                second=55,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
        )

        # Act
        json_str = frbc_system_description.to_json()

        # Assert
        expected_json = {
            "actuators": [
                {
                    "diagnostic_label": "some-test-string2728",
                    "id": "a1061148-f19e-4b1b-8fe3-b506583ce61e",
                    "operation_modes": [
                        {
                            "abnormal_condition_only": False,
                            "diagnostic_label": "some-test-string2930",
                            "elements": [
                                {
                                    "fill_level_range": {
                                        "end_of_range": 36932.65171036228,
                                        "start_of_range": 12649.272766336762,
                                    },
                                    "fill_rate": {
                                        "end_of_range": 34553.16163528188,
                                        "start_of_range": 14377.963894945604,
                                    },
                                    "power_ranges": [
                                        {
                                            "commodity_quantity": "ELECTRIC.POWER.L1",
                                            "end_of_range": 46924.65023353163,
                                            "start_of_range": 11888.235871902496,
                                        }
                                    ],
                                    "running_costs": {
                                        "end_of_range": 42897.60731684277,
                                        "start_of_range": 33997.56376994998,
                                    },
                                }
                            ],
                            "id": "2795136c-eb30-4f8a-bdaa-61feba1e71b6",
                        }
                    ],
                    "supported_commodities": ["ELECTRICITY"],
                    "timers": [
                        {
                            "diagnostic_label": "some-test-string4315",
                            "duration": 14099,
                            "id": "e1ff9e58-935b-4765-92e3-5e7679f73eb6",
                        }
                    ],
                    "transitions": [
                        {
                            "abnormal_condition_only": True,
                            "blocking_timers": ["e1ff9e58-935b-4765-92e3-5e7679f73eb6"],
                            "from": "2795136c-eb30-4f8a-bdaa-61feba1e71b6",
                            "id": "c32cc1d3-4722-41e3-a8de-55307c723611",
                            "start_timers": ["e1ff9e58-935b-4765-92e3-5e7679f73eb6"],
                            "to": "2795136c-eb30-4f8a-bdaa-61feba1e71b6",
                            "transition_costs": 1018.4228054114793,
                            "transition_duration": 11988,
                        }
                    ],
                }
            ],
            "message_id": "97256813-de70-4640-a992-9ae0b2d8e4d1",
            "message_type": "FRBC.SystemDescription",
            "storage": {
                "diagnostic_label": "some-test-string8418",
                "fill_level_label": "some-test-string9512",
                "fill_level_range": {
                    "end_of_range": 20876.752745956997,
                    "start_of_range": 18324.0229135081,
                },
                "provides_fill_level_target_profile": False,
                "provides_leakage_behaviour": True,
                "provides_usage_forecast": False,
            },
            "valid_from": "2020-10-07T06:30:55Z",
        }
        self.assertEqual(json.loads(json_str), expected_json)
