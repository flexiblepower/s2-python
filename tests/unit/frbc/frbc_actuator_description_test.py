
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
    "id": "d94c8444-fecd-4e2b-a753-3ba95c80a8b9",
    "diagnostic_label": "some-test-string7020",
    "supported_commodities": [
        "GAS"
    ],
    "operation_modes": [
        {
            "id": "0896dcbb-74d8-4875-8d46-3e2ffe0d6fc6",
            "diagnostic_label": "some-test-string5647",
            "elements": [
                {
                    "fill_level_range": {
                        "start_of_range": 29629.998638216148,
                        "end_of_range": 47173.64237787903
                    },
                    "fill_rate": {
                        "start_of_range": 6928.475192465882,
                        "end_of_range": 27602.436966784364
                    },
                    "power_ranges": [
                        {
                            "start_of_range": 4601.097096109952,
                            "end_of_range": 40109.78028113443,
                            "commodity_quantity": "ELECTRIC.POWER.L1"
                        }
                    ],
                    "running_costs": {
                        "start_of_range": 32340.91070921078,
                        "end_of_range": 68671.08362229214
                    }
                }
            ],
            "abnormal_condition_only": false
        }
    ],
    "transitions": [
        {
            "id": "ba747269-ce4b-405c-bc8a-38cba20342a7",
            "from_": "c8b76640-8eb1-4656-9477-2bc2afdca867",
            "to": "e53e871e-b09e-4a81-9a6d-4b317b30ee04",
            "start_timers": [
                "fce4d143-a7d4-4c53-a66c-da2faec9cc61"
            ],
            "blocking_timers": [
                "c33dc9cd-b82f-4649-b610-a70f3787facd"
            ],
            "transition_costs": 4575.2975690198045,
            "transition_duration": 10950,
            "abnormal_condition_only": false
        }
    ],
    "timers": [
        {
            "id": "033d2a04-a874-4537-a475-ecc5fc538282",
            "diagnostic_label": "some-test-string380",
            "duration": 28910
        }
    ]
}
        """

        # Act
        frbc_actuator_description = FRBCActuatorDescription.from_json(json_str)

        # Assert
        self.assertEqual(frbc_actuator_description.id, uuid.UUID("d94c8444-fecd-4e2b-a753-3ba95c80a8b9"))
        self.assertEqual(frbc_actuator_description.diagnostic_label, "some-test-string7020")
        self.assertEqual(frbc_actuator_description.supported_commodities, [Commodity.GAS])
        self.assertEqual(frbc_actuator_description.operation_modes, [FRBCOperationMode(id=uuid.UUID("0896dcbb-74d8-4875-8d46-3e2ffe0d6fc6"), diagnostic_label="some-test-string5647", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=29629.998638216148, end_of_range=47173.64237787903), fill_rate=NumberRange(start_of_range=6928.475192465882, end_of_range=27602.436966784364), power_ranges=[PowerRange(start_of_range=4601.097096109952, end_of_range=40109.78028113443, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=32340.91070921078, end_of_range=68671.08362229214))], abnormal_condition_only=False)])
        self.assertEqual(frbc_actuator_description.transitions, [Transition(id=uuid.UUID("ba747269-ce4b-405c-bc8a-38cba20342a7"), from_=uuid.UUID("c8b76640-8eb1-4656-9477-2bc2afdca867"), to=uuid.UUID("e53e871e-b09e-4a81-9a6d-4b317b30ee04"), start_timers=[uuid.UUID("fce4d143-a7d4-4c53-a66c-da2faec9cc61")], blocking_timers=[uuid.UUID("c33dc9cd-b82f-4649-b610-a70f3787facd")], transition_costs=4575.2975690198045, transition_duration=Duration.from_timedelta(timedelta(milliseconds=10950)), abnormal_condition_only=False)])
        self.assertEqual(frbc_actuator_description.timers, [Timer(id=uuid.UUID("033d2a04-a874-4537-a475-ecc5fc538282"), diagnostic_label="some-test-string380", duration=Duration.from_timedelta(timedelta(milliseconds=28910)))])

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_actuator_description = FRBCActuatorDescription(id=uuid.UUID("d94c8444-fecd-4e2b-a753-3ba95c80a8b9"), diagnostic_label="some-test-string7020", supported_commodities=[Commodity.GAS], operation_modes=[FRBCOperationMode(id=uuid.UUID("0896dcbb-74d8-4875-8d46-3e2ffe0d6fc6"), diagnostic_label="some-test-string5647", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=29629.998638216148, end_of_range=47173.64237787903), fill_rate=NumberRange(start_of_range=6928.475192465882, end_of_range=27602.436966784364), power_ranges=[PowerRange(start_of_range=4601.097096109952, end_of_range=40109.78028113443, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=32340.91070921078, end_of_range=68671.08362229214))], abnormal_condition_only=False)], transitions=[Transition(id=uuid.UUID("ba747269-ce4b-405c-bc8a-38cba20342a7"), from_=uuid.UUID("c8b76640-8eb1-4656-9477-2bc2afdca867"), to=uuid.UUID("e53e871e-b09e-4a81-9a6d-4b317b30ee04"), start_timers=[uuid.UUID("fce4d143-a7d4-4c53-a66c-da2faec9cc61")], blocking_timers=[uuid.UUID("c33dc9cd-b82f-4649-b610-a70f3787facd")], transition_costs=4575.2975690198045, transition_duration=Duration.from_timedelta(timedelta(milliseconds=10950)), abnormal_condition_only=False)], timers=[Timer(id=uuid.UUID("033d2a04-a874-4537-a475-ecc5fc538282"), diagnostic_label="some-test-string380", duration=Duration.from_timedelta(timedelta(milliseconds=28910)))])

        # Act
        json_str = frbc_actuator_description.to_json()

        # Assert
        expected_json = {   'diagnostic_label': 'some-test-string7020',
    'id': 'd94c8444-fecd-4e2b-a753-3ba95c80a8b9',
    'operation_modes': [   {   'abnormal_condition_only': False,
                               'diagnostic_label': 'some-test-string5647',
                               'elements': [   {   'fill_level_range': {   'end_of_range': 47173.64237787903,
                                                                           'start_of_range': 29629.998638216148},
                                                   'fill_rate': {   'end_of_range': 27602.436966784364,
                                                                    'start_of_range': 6928.475192465882},
                                                   'power_ranges': [   {   'commodity_quantity': 'ELECTRIC.POWER.L1',
                                                                           'end_of_range': 40109.78028113443,
                                                                           'start_of_range': 4601.097096109952}],
                                                   'running_costs': {   'end_of_range': 68671.08362229214,
                                                                        'start_of_range': 32340.91070921078}}],
                               'id': '0896dcbb-74d8-4875-8d46-3e2ffe0d6fc6'}],
    'supported_commodities': ['GAS'],
    'timers': [   {   'diagnostic_label': 'some-test-string380',
                      'duration': 28910,
                      'id': '033d2a04-a874-4537-a475-ecc5fc538282'}],
    'transitions': [   {   'abnormal_condition_only': False,
                           'blocking_timers': [   'c33dc9cd-b82f-4649-b610-a70f3787facd'],
                           'from_': 'c8b76640-8eb1-4656-9477-2bc2afdca867',
                           'id': 'ba747269-ce4b-405c-bc8a-38cba20342a7',
                           'start_timers': [   'fce4d143-a7d4-4c53-a66c-da2faec9cc61'],
                           'to': 'e53e871e-b09e-4a81-9a6d-4b317b30ee04',
                           'transition_costs': 4575.2975690198045,
                           'transition_duration': 10950}]}
        self.assertEqual(json.loads(json_str), expected_json)
