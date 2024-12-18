
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
    "message_type": "FRBC.SystemDescription",
    "message_id": "873112de-a6d8-4123-a523-fc908e9a0310",
    "valid_from": "2021-07-20T04:50:11+12:00",
    "actuators": [
        {
            "id": "9d5243b4-f92c-42cd-9d6b-00e3e5953dd4",
            "diagnostic_label": "some-test-string2832",
            "supported_commodities": [
                "GAS"
            ],
            "operation_modes": [
                {
                    "id": "4526bc26-cdd8-4cd6-ae35-dfb2a6751375",
                    "diagnostic_label": "some-test-string2393",
                    "elements": [
                        {
                            "fill_level_range": {
                                "start_of_range": 22530.41813108864,
                                "end_of_range": 50141.518189827795
                            },
                            "fill_rate": {
                                "start_of_range": 10937.461391570358,
                                "end_of_range": 22111.530603779658
                            },
                            "power_ranges": [
                                {
                                    "start_of_range": 3372.255894277375,
                                    "end_of_range": 11155.631994233203,
                                    "commodity_quantity": "ELECTRIC.POWER.L1"
                                }
                            ],
                            "running_costs": {
                                "start_of_range": 31076.328103540887,
                                "end_of_range": 38380.84063645549
                            }
                        }
                    ],
                    "abnormal_condition_only": false
                }
            ],
            "transitions": [
                {
                    "id": "5b9bd90f-d9ec-4eb0-915e-f6b7d7cfab3e",
                    "from_": "cac664cf-bec3-49df-aeb4-d5dca13f3f0b",
                    "to": "61605548-7d68-4ceb-bbe2-b4d79d385b11",
                    "start_timers": [
                        "d2436620-dce4-43fe-a59d-a7bc3045a7cd"
                    ],
                    "blocking_timers": [
                        "2f690536-73d5-4441-90b4-a28fa60e962f"
                    ],
                    "transition_costs": 2339.5028721662775,
                    "transition_duration": 35219,
                    "abnormal_condition_only": true
                }
            ],
            "timers": [
                {
                    "id": "0c8a46de-b2bf-4adc-9052-0d2aa5dade66",
                    "diagnostic_label": "some-test-string8913",
                    "duration": 20103
                }
            ]
        }
    ],
    "storage": {
        "diagnostic_label": "some-test-string816",
        "fill_level_label": "some-test-string5484",
        "provides_leakage_behaviour": true,
        "provides_fill_level_target_profile": true,
        "provides_usage_forecast": true,
        "fill_level_range": {
            "start_of_range": 16537.091716121224,
            "end_of_range": 19907.512143139258
        }
    }
}
        """

        # Act
        frbc_system_description = FRBCSystemDescription.from_json(json_str)

        # Assert
        self.assertEqual(frbc_system_description.message_type, FRBC.SystemDescription)
        self.assertEqual(frbc_system_description.message_id, uuid.UUID("873112de-a6d8-4123-a523-fc908e9a0310"))
        self.assertEqual(frbc_system_description.valid_from, datetime(year=2021, month=7, day=20, hour=4, minute=50, second=11, tzinfo=offset(offset=timedelta(seconds=43200.0))))
        self.assertEqual(frbc_system_description.actuators, [FRBCActuatorDescription(id=uuid.UUID("9d5243b4-f92c-42cd-9d6b-00e3e5953dd4"), diagnostic_label="some-test-string2832", supported_commodities=[Commodity.GAS], operation_modes=[FRBCOperationMode(id=uuid.UUID("4526bc26-cdd8-4cd6-ae35-dfb2a6751375"), diagnostic_label="some-test-string2393", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=22530.41813108864, end_of_range=50141.518189827795), fill_rate=NumberRange(start_of_range=10937.461391570358, end_of_range=22111.530603779658), power_ranges=[PowerRange(start_of_range=3372.255894277375, end_of_range=11155.631994233203, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=31076.328103540887, end_of_range=38380.84063645549))], abnormal_condition_only=False)], transitions=[Transition(id=uuid.UUID("5b9bd90f-d9ec-4eb0-915e-f6b7d7cfab3e"), from_=uuid.UUID("cac664cf-bec3-49df-aeb4-d5dca13f3f0b"), to=uuid.UUID("61605548-7d68-4ceb-bbe2-b4d79d385b11"), start_timers=[uuid.UUID("d2436620-dce4-43fe-a59d-a7bc3045a7cd")], blocking_timers=[uuid.UUID("2f690536-73d5-4441-90b4-a28fa60e962f")], transition_costs=2339.5028721662775, transition_duration=Duration.from_timedelta(timedelta(milliseconds=35219)), abnormal_condition_only=True)], timers=[Timer(id=uuid.UUID("0c8a46de-b2bf-4adc-9052-0d2aa5dade66"), diagnostic_label="some-test-string8913", duration=Duration.from_timedelta(timedelta(milliseconds=20103)))])])
        self.assertEqual(frbc_system_description.storage, FRBCStorageDescription(diagnostic_label="some-test-string816", fill_level_label="some-test-string5484", provides_leakage_behaviour=True, provides_fill_level_target_profile=True, provides_usage_forecast=True, fill_level_range=NumberRange(start_of_range=16537.091716121224, end_of_range=19907.512143139258)))

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_system_description = FRBCSystemDescription(message_type=FRBC.SystemDescription, message_id=uuid.UUID("873112de-a6d8-4123-a523-fc908e9a0310"), valid_from=datetime(year=2021, month=7, day=20, hour=4, minute=50, second=11, tzinfo=offset(offset=timedelta(seconds=43200.0))), actuators=[FRBCActuatorDescription(id=uuid.UUID("9d5243b4-f92c-42cd-9d6b-00e3e5953dd4"), diagnostic_label="some-test-string2832", supported_commodities=[Commodity.GAS], operation_modes=[FRBCOperationMode(id=uuid.UUID("4526bc26-cdd8-4cd6-ae35-dfb2a6751375"), diagnostic_label="some-test-string2393", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=22530.41813108864, end_of_range=50141.518189827795), fill_rate=NumberRange(start_of_range=10937.461391570358, end_of_range=22111.530603779658), power_ranges=[PowerRange(start_of_range=3372.255894277375, end_of_range=11155.631994233203, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=31076.328103540887, end_of_range=38380.84063645549))], abnormal_condition_only=False)], transitions=[Transition(id=uuid.UUID("5b9bd90f-d9ec-4eb0-915e-f6b7d7cfab3e"), from_=uuid.UUID("cac664cf-bec3-49df-aeb4-d5dca13f3f0b"), to=uuid.UUID("61605548-7d68-4ceb-bbe2-b4d79d385b11"), start_timers=[uuid.UUID("d2436620-dce4-43fe-a59d-a7bc3045a7cd")], blocking_timers=[uuid.UUID("2f690536-73d5-4441-90b4-a28fa60e962f")], transition_costs=2339.5028721662775, transition_duration=Duration.from_timedelta(timedelta(milliseconds=35219)), abnormal_condition_only=True)], timers=[Timer(id=uuid.UUID("0c8a46de-b2bf-4adc-9052-0d2aa5dade66"), diagnostic_label="some-test-string8913", duration=Duration.from_timedelta(timedelta(milliseconds=20103)))])], storage=FRBCStorageDescription(diagnostic_label="some-test-string816", fill_level_label="some-test-string5484", provides_leakage_behaviour=True, provides_fill_level_target_profile=True, provides_usage_forecast=True, fill_level_range=NumberRange(start_of_range=16537.091716121224, end_of_range=19907.512143139258)))

        # Act
        json_str = frbc_system_description.to_json()

        # Assert
        expected_json = {   'actuators': [   {   'diagnostic_label': 'some-test-string2832',
                         'id': '9d5243b4-f92c-42cd-9d6b-00e3e5953dd4',
                         'operation_modes': [   {   'abnormal_condition_only': False,
                                                    'diagnostic_label': 'some-test-string2393',
                                                    'elements': [   {   'fill_level_range': {   'end_of_range': 50141.518189827795,
                                                                                                'start_of_range': 22530.41813108864},
                                                                        'fill_rate': {   'end_of_range': 22111.530603779658,
                                                                                         'start_of_range': 10937.461391570358},
                                                                        'power_ranges': [   {   'commodity_quantity': 'ELECTRIC.POWER.L1',
                                                                                                'end_of_range': 11155.631994233203,
                                                                                                'start_of_range': 3372.255894277375}],
                                                                        'running_costs': {   'end_of_range': 38380.84063645549,
                                                                                             'start_of_range': 31076.328103540887}}],
                                                    'id': '4526bc26-cdd8-4cd6-ae35-dfb2a6751375'}],
                         'supported_commodities': ['GAS'],
                         'timers': [   {   'diagnostic_label': 'some-test-string8913',
                                           'duration': 20103,
                                           'id': '0c8a46de-b2bf-4adc-9052-0d2aa5dade66'}],
                         'transitions': [   {   'abnormal_condition_only': True,
                                                'blocking_timers': [   '2f690536-73d5-4441-90b4-a28fa60e962f'],
                                                'from_': 'cac664cf-bec3-49df-aeb4-d5dca13f3f0b',
                                                'id': '5b9bd90f-d9ec-4eb0-915e-f6b7d7cfab3e',
                                                'start_timers': [   'd2436620-dce4-43fe-a59d-a7bc3045a7cd'],
                                                'to': '61605548-7d68-4ceb-bbe2-b4d79d385b11',
                                                'transition_costs': 2339.5028721662775,
                                                'transition_duration': 35219}]}],
    'message_id': '873112de-a6d8-4123-a523-fc908e9a0310',
    'message_type': 'FRBC.SystemDescription',
    'storage': {   'diagnostic_label': 'some-test-string816',
                   'fill_level_label': 'some-test-string5484',
                   'fill_level_range': {   'end_of_range': 19907.512143139258,
                                           'start_of_range': 16537.091716121224},
                   'provides_fill_level_target_profile': True,
                   'provides_leakage_behaviour': True,
                   'provides_usage_forecast': True},
    'valid_from': '2021-07-20T04:50:11+12:00'}
        self.assertEqual(json.loads(json_str), expected_json)
