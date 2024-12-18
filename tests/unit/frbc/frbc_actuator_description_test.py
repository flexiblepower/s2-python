
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
    "id": "5ebe5f2d-3046-48b3-b2ce-5f4c58630fc9",
    "diagnostic_label": "some-test-string8906",
    "supported_commodities": [
        "GAS"
    ],
    "operation_modes": [
        {
            "id": "512001f9-e720-40ce-88e2-06694bb2ca6d",
            "diagnostic_label": "some-test-string1472",
            "elements": [
                {
                    "fill_level_range": {
                        "start_of_range": 27494.741307134802,
                        "end_of_range": 58877.84844659244
                    },
                    "fill_rate": {
                        "start_of_range": 25438.73202815934,
                        "end_of_range": 32365.85082869052
                    },
                    "power_ranges": [
                        {
                            "start_of_range": 810.7301251031068,
                            "end_of_range": 36176.5333835611,
                            "commodity_quantity": "ELECTRIC.POWER.L1"
                        }
                    ],
                    "running_costs": {
                        "start_of_range": 37284.94705878388,
                        "end_of_range": 61334.00977608085
                    }
                }
            ],
            "abnormal_condition_only": false
        }
    ],
    "transitions": [
        {
            "id": "5427f2cc-7d7d-4d30-bdc8-5f6594a86297",
            "from_": "de2771e5-bac3-4385-8ee1-ad1500b2905f",
            "to": "a169553d-cac4-4b29-9cce-9a9a17b5aebd",
            "start_timers": [
                "26538354-e139-448d-9cb1-19da008bbd43"
            ],
            "blocking_timers": [
                "947ad518-3305-4be4-b847-a4b01a0bfd01"
            ],
            "transition_costs": 3119.39267710221,
            "transition_duration": 21417,
            "abnormal_condition_only": false
        }
    ],
    "timers": [
        {
            "id": "166fdf46-2695-412e-a014-dbd95dee1eb2",
            "diagnostic_label": "some-test-string9309",
            "duration": 16076
        }
    ]
}
        """

        # Act
        frbc_actuator_description = FRBCActuatorDescription.from_json(json_str)

        # Assert
        self.assertEqual(frbc_actuator_description.id, uuid.UUID("5ebe5f2d-3046-48b3-b2ce-5f4c58630fc9"))
        self.assertEqual(frbc_actuator_description.diagnostic_label, "some-test-string8906")
        self.assertEqual(frbc_actuator_description.supported_commodities, [Commodity.GAS])
        self.assertEqual(frbc_actuator_description.operation_modes, [FRBCOperationMode(id=uuid.UUID("512001f9-e720-40ce-88e2-06694bb2ca6d"), diagnostic_label="some-test-string1472", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=27494.741307134802, end_of_range=58877.84844659244), fill_rate=NumberRange(start_of_range=25438.73202815934, end_of_range=32365.85082869052), power_ranges=[PowerRange(start_of_range=810.7301251031068, end_of_range=36176.5333835611, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=37284.94705878388, end_of_range=61334.00977608085))], abnormal_condition_only=False)])
        self.assertEqual(frbc_actuator_description.transitions, [Transition(id=uuid.UUID("5427f2cc-7d7d-4d30-bdc8-5f6594a86297"), from_=uuid.UUID("de2771e5-bac3-4385-8ee1-ad1500b2905f"), to=uuid.UUID("a169553d-cac4-4b29-9cce-9a9a17b5aebd"), start_timers=[uuid.UUID("26538354-e139-448d-9cb1-19da008bbd43")], blocking_timers=[uuid.UUID("947ad518-3305-4be4-b847-a4b01a0bfd01")], transition_costs=3119.39267710221, transition_duration=Duration.from_timedelta(timedelta(milliseconds=21417)), abnormal_condition_only=False)])
        self.assertEqual(frbc_actuator_description.timers, [Timer(id=uuid.UUID("166fdf46-2695-412e-a014-dbd95dee1eb2"), diagnostic_label="some-test-string9309", duration=Duration.from_timedelta(timedelta(milliseconds=16076)))])

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_actuator_description = FRBCActuatorDescription(id=uuid.UUID("5ebe5f2d-3046-48b3-b2ce-5f4c58630fc9"), diagnostic_label="some-test-string8906", supported_commodities=[Commodity.GAS], operation_modes=[FRBCOperationMode(id=uuid.UUID("512001f9-e720-40ce-88e2-06694bb2ca6d"), diagnostic_label="some-test-string1472", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=27494.741307134802, end_of_range=58877.84844659244), fill_rate=NumberRange(start_of_range=25438.73202815934, end_of_range=32365.85082869052), power_ranges=[PowerRange(start_of_range=810.7301251031068, end_of_range=36176.5333835611, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=37284.94705878388, end_of_range=61334.00977608085))], abnormal_condition_only=False)], transitions=[Transition(id=uuid.UUID("5427f2cc-7d7d-4d30-bdc8-5f6594a86297"), from_=uuid.UUID("de2771e5-bac3-4385-8ee1-ad1500b2905f"), to=uuid.UUID("a169553d-cac4-4b29-9cce-9a9a17b5aebd"), start_timers=[uuid.UUID("26538354-e139-448d-9cb1-19da008bbd43")], blocking_timers=[uuid.UUID("947ad518-3305-4be4-b847-a4b01a0bfd01")], transition_costs=3119.39267710221, transition_duration=Duration.from_timedelta(timedelta(milliseconds=21417)), abnormal_condition_only=False)], timers=[Timer(id=uuid.UUID("166fdf46-2695-412e-a014-dbd95dee1eb2"), diagnostic_label="some-test-string9309", duration=Duration.from_timedelta(timedelta(milliseconds=16076)))])

        # Act
        json_str = frbc_actuator_description.to_json()

        # Assert
        expected_json = {   'diagnostic_label': 'some-test-string8906',
    'id': '5ebe5f2d-3046-48b3-b2ce-5f4c58630fc9',
    'operation_modes': [   {   'abnormal_condition_only': False,
                               'diagnostic_label': 'some-test-string1472',
                               'elements': [   {   'fill_level_range': {   'end_of_range': 58877.84844659244,
                                                                           'start_of_range': 27494.741307134802},
                                                   'fill_rate': {   'end_of_range': 32365.85082869052,
                                                                    'start_of_range': 25438.73202815934},
                                                   'power_ranges': [   {   'commodity_quantity': 'ELECTRIC.POWER.L1',
                                                                           'end_of_range': 36176.5333835611,
                                                                           'start_of_range': 810.7301251031068}],
                                                   'running_costs': {   'end_of_range': 61334.00977608085,
                                                                        'start_of_range': 37284.94705878388}}],
                               'id': '512001f9-e720-40ce-88e2-06694bb2ca6d'}],
    'supported_commodities': ['GAS'],
    'timers': [   {   'diagnostic_label': 'some-test-string9309',
                      'duration': 16076,
                      'id': '166fdf46-2695-412e-a014-dbd95dee1eb2'}],
    'transitions': [   {   'abnormal_condition_only': False,
                           'blocking_timers': [   '947ad518-3305-4be4-b847-a4b01a0bfd01'],
                           'from_': 'de2771e5-bac3-4385-8ee1-ad1500b2905f',
                           'id': '5427f2cc-7d7d-4d30-bdc8-5f6594a86297',
                           'start_timers': [   '26538354-e139-448d-9cb1-19da008bbd43'],
                           'to': 'a169553d-cac4-4b29-9cce-9a9a17b5aebd',
                           'transition_costs': 3119.39267710221,
                           'transition_duration': 21417}]}
        self.assertEqual(json.loads(json_str), expected_json)
