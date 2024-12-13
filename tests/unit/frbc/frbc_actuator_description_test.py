
from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCActuatorDescriptionTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "id": "a58e9c5e-511b-436c-9c65-ad44c778c4b8",
    "diagnostic_label": "some-test-string3006",
    "supported_commodities": [
        "GAS"
    ],
    "operation_modes": [
        {
            "id": "5d104a14-491f-4138-a757-ff0cb6fd5525",
            "diagnostic_label": "some-test-string7637",
            "elements": [
                {
                    "fill_level_range": {
                        "start_of_range": 24714.62330770477,
                        "end_of_range": 49561.87219293591
                    },
                    "fill_rate": {
                        "start_of_range": 22860.909596605932,
                        "end_of_range": 50712.187596827665
                    },
                    "power_ranges": [
                        {
                            "start_of_range": 31917.547195435036,
                            "end_of_range": 56269.308985594,
                            "commodity_quantity": "ELECTRIC.POWER.L1"
                        }
                    ],
                    "running_costs": {
                        "start_of_range": 1119.8343828050738,
                        "end_of_range": 24787.439438905614
                    }
                }
            ],
            "abnormal_condition_only": false
        }
    ],
    "transitions": [
        {
            "id": "47f2c50d-17b4-4892-97f0-f3f81abb5c36",
            "from_": "8b235e80-5c21-452f-8c58-72e887ab5aab",
            "to": "9c585f61-e1b1-4e53-9fb4-5d60e141d51f",
            "start_timers": [
                "f94f42ff-f836-4ba9-97f9-da3aa24941d6"
            ],
            "blocking_timers": [
                "ce322294-db0f-4351-a971-8c175c52714f"
            ],
            "transition_costs": 347.97008821629373,
            "transition_duration": 39801,
            "abnormal_condition_only": false
        }
    ],
    "timers": [
        {
            "id": "73933f13-7c3a-4f76-9975-99acf562498e",
            "diagnostic_label": "some-test-string3849",
            "duration": 23667
        }
    ]
}
        """

        # Act
        frbc_actuator_description = FRBCActuatorDescription.from_json(json_str)

        # Assert
        self.assertEqual(frbc_actuator_description.id, uuid.UUID("a58e9c5e-511b-436c-9c65-ad44c778c4b8"))
        self.assertEqual(frbc_actuator_description.diagnostic_label, "some-test-string3006")
        self.assertEqual(frbc_actuator_description.supported_commodities, [Commodity.GAS])
        self.assertEqual(frbc_actuator_description.operation_modes, [FRBCOperationMode(id=uuid.UUID("5d104a14-491f-4138-a757-ff0cb6fd5525"), diagnostic_label="some-test-string7637", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=24714.62330770477, end_of_range=49561.87219293591), fill_rate=NumberRange(start_of_range=22860.909596605932, end_of_range=50712.187596827665), power_ranges=[PowerRange(start_of_range=31917.547195435036, end_of_range=56269.308985594, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=1119.8343828050738, end_of_range=24787.439438905614))], abnormal_condition_only=False)])
        self.assertEqual(frbc_actuator_description.transitions, [Transition(id=uuid.UUID("47f2c50d-17b4-4892-97f0-f3f81abb5c36"), from_=uuid.UUID("8b235e80-5c21-452f-8c58-72e887ab5aab"), to=uuid.UUID("9c585f61-e1b1-4e53-9fb4-5d60e141d51f"), start_timers=[uuid.UUID("f94f42ff-f836-4ba9-97f9-da3aa24941d6")], blocking_timers=[uuid.UUID("ce322294-db0f-4351-a971-8c175c52714f")], transition_costs=347.97008821629373, transition_duration=Duration.from_timedelta(timedelta(milliseconds=39801)), abnormal_condition_only=False)])
        self.assertEqual(frbc_actuator_description.timers, [Timer(id=uuid.UUID("73933f13-7c3a-4f76-9975-99acf562498e"), diagnostic_label="some-test-string3849", duration=Duration.from_timedelta(timedelta(milliseconds=23667)))])

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_actuator_description = FRBCActuatorDescription(id=uuid.UUID("a58e9c5e-511b-436c-9c65-ad44c778c4b8"), diagnostic_label="some-test-string3006", supported_commodities=[Commodity.GAS], operation_modes=[FRBCOperationMode(id=uuid.UUID("5d104a14-491f-4138-a757-ff0cb6fd5525"), diagnostic_label="some-test-string7637", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=24714.62330770477, end_of_range=49561.87219293591), fill_rate=NumberRange(start_of_range=22860.909596605932, end_of_range=50712.187596827665), power_ranges=[PowerRange(start_of_range=31917.547195435036, end_of_range=56269.308985594, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=1119.8343828050738, end_of_range=24787.439438905614))], abnormal_condition_only=False)], transitions=[Transition(id=uuid.UUID("47f2c50d-17b4-4892-97f0-f3f81abb5c36"), from_=uuid.UUID("8b235e80-5c21-452f-8c58-72e887ab5aab"), to=uuid.UUID("9c585f61-e1b1-4e53-9fb4-5d60e141d51f"), start_timers=[uuid.UUID("f94f42ff-f836-4ba9-97f9-da3aa24941d6")], blocking_timers=[uuid.UUID("ce322294-db0f-4351-a971-8c175c52714f")], transition_costs=347.97008821629373, transition_duration=Duration.from_timedelta(timedelta(milliseconds=39801)), abnormal_condition_only=False)], timers=[Timer(id=uuid.UUID("73933f13-7c3a-4f76-9975-99acf562498e"), diagnostic_label="some-test-string3849", duration=Duration.from_timedelta(timedelta(milliseconds=23667)))])

        # Act
        json_str = frbc_actuator_description.to_json()

        # Assert
        expected_json = {   'diagnostic_label': 'some-test-string3006',
    'id': 'a58e9c5e-511b-436c-9c65-ad44c778c4b8',
    'operation_modes': [   {   'abnormal_condition_only': False,
                               'diagnostic_label': 'some-test-string7637',
                               'elements': [   {   'fill_level_range': {   'end_of_range': 49561.87219293591,
                                                                           'start_of_range': 24714.62330770477},
                                                   'fill_rate': {   'end_of_range': 50712.187596827665,
                                                                    'start_of_range': 22860.909596605932},
                                                   'power_ranges': [   {   'commodity_quantity': 'ELECTRIC.POWER.L1',
                                                                           'end_of_range': 56269.308985594,
                                                                           'start_of_range': 31917.547195435036}],
                                                   'running_costs': {   'end_of_range': 24787.439438905614,
                                                                        'start_of_range': 1119.8343828050738}}],
                               'id': '5d104a14-491f-4138-a757-ff0cb6fd5525'}],
    'supported_commodities': ['GAS'],
    'timers': [   {   'diagnostic_label': 'some-test-string3849',
                      'duration': 23667,
                      'id': '73933f13-7c3a-4f76-9975-99acf562498e'}],
    'transitions': [   {   'abnormal_condition_only': False,
                           'blocking_timers': [   'ce322294-db0f-4351-a971-8c175c52714f'],
                           'from_': '8b235e80-5c21-452f-8c58-72e887ab5aab',
                           'id': '47f2c50d-17b4-4892-97f0-f3f81abb5c36',
                           'start_timers': [   'f94f42ff-f836-4ba9-97f9-da3aa24941d6'],
                           'to': '9c585f61-e1b1-4e53-9fb4-5d60e141d51f',
                           'transition_costs': 347.97008821629373,
                           'transition_duration': 39801}]}
        self.assertEqual(json.loads(json_str), expected_json)
