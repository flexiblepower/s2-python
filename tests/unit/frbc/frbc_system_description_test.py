
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
    "message_id": "a2dfaa9c-e52c-435d-94e4-15007f208ec6",
    "valid_from": "2021-07-13T15:48:07+00:00",
    "actuators": [
        {
            "id": "b6872218-3fb7-436e-bdcb-e393f8ef95f7",
            "diagnostic_label": "some-test-string6489",
            "supported_commodities": [
                "GAS"
            ],
            "operation_modes": [
                {
                    "id": "052029e8-85e2-4b96-bd03-7f3345445e76",
                    "diagnostic_label": "some-test-string7949",
                    "elements": [
                        {
                            "fill_level_range": {
                                "start_of_range": 17740.22962461282,
                                "end_of_range": 52507.59091283206
                            },
                            "fill_rate": {
                                "start_of_range": 35532.15914996989,
                                "end_of_range": 48265.232076205815
                            },
                            "power_ranges": [
                                {
                                    "start_of_range": 38748.50842724231,
                                    "end_of_range": 47741.69817105044,
                                    "commodity_quantity": "ELECTRIC.POWER.L1"
                                }
                            ],
                            "running_costs": {
                                "start_of_range": 35692.82350352573,
                                "end_of_range": 47884.66649499221
                            }
                        }
                    ],
                    "abnormal_condition_only": true
                }
            ],
            "transitions": [
                {
                    "id": "b1ace854-611e-4064-8c9b-434b453879df",
                    "from_": "66c5b0af-36e0-425d-b5c3-9cf27944f555",
                    "to": "8aed333c-663c-4502-8dc2-45c21acbe366",
                    "start_timers": [
                        "56258c00-182b-4299-b9f0-c44d533dfdcb"
                    ],
                    "blocking_timers": [
                        "8dac5674-4428-46cd-bfad-c89bb4d23029"
                    ],
                    "transition_costs": 1403.4899643577787,
                    "transition_duration": 32794,
                    "abnormal_condition_only": false
                }
            ],
            "timers": [
                {
                    "id": "e8a806df-eb45-4ed6-959d-db717d2462c8",
                    "diagnostic_label": "some-test-string3261",
                    "duration": 5659
                }
            ]
        }
    ],
    "storage": {
        "diagnostic_label": "some-test-string9735",
        "fill_level_label": "some-test-string1238",
        "provides_leakage_behaviour": true,
        "provides_fill_level_target_profile": false,
        "provides_usage_forecast": true,
        "fill_level_range": {
            "start_of_range": 8670.277473912942,
            "end_of_range": 27152.584459033194
        }
    }
}
        """

        # Act
        frbc_system_description = FRBCSystemDescription.from_json(json_str)

        # Assert
        self.assertEqual(frbc_system_description.message_type, FRBC.SystemDescription)
        self.assertEqual(frbc_system_description.message_id, uuid.UUID("a2dfaa9c-e52c-435d-94e4-15007f208ec6"))
        self.assertEqual(frbc_system_description.valid_from, datetime(year=2021, month=7, day=13, hour=15, minute=48, second=7, tzinfo=offset(offset=timedelta(seconds=0.0))))
        self.assertEqual(frbc_system_description.actuators, [FRBCActuatorDescription(id=uuid.UUID("b6872218-3fb7-436e-bdcb-e393f8ef95f7"), diagnostic_label="some-test-string6489", supported_commodities=[Commodity.GAS], operation_modes=[FRBCOperationMode(id=uuid.UUID("052029e8-85e2-4b96-bd03-7f3345445e76"), diagnostic_label="some-test-string7949", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=17740.22962461282, end_of_range=52507.59091283206), fill_rate=NumberRange(start_of_range=35532.15914996989, end_of_range=48265.232076205815), power_ranges=[PowerRange(start_of_range=38748.50842724231, end_of_range=47741.69817105044, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=35692.82350352573, end_of_range=47884.66649499221))], abnormal_condition_only=True)], transitions=[Transition(id=uuid.UUID("b1ace854-611e-4064-8c9b-434b453879df"), from_=uuid.UUID("66c5b0af-36e0-425d-b5c3-9cf27944f555"), to=uuid.UUID("8aed333c-663c-4502-8dc2-45c21acbe366"), start_timers=[uuid.UUID("56258c00-182b-4299-b9f0-c44d533dfdcb")], blocking_timers=[uuid.UUID("8dac5674-4428-46cd-bfad-c89bb4d23029")], transition_costs=1403.4899643577787, transition_duration=Duration.from_timedelta(timedelta(milliseconds=32794)), abnormal_condition_only=False)], timers=[Timer(id=uuid.UUID("e8a806df-eb45-4ed6-959d-db717d2462c8"), diagnostic_label="some-test-string3261", duration=Duration.from_timedelta(timedelta(milliseconds=5659)))])])
        self.assertEqual(frbc_system_description.storage, FRBCStorageDescription(diagnostic_label="some-test-string9735", fill_level_label="some-test-string1238", provides_leakage_behaviour=True, provides_fill_level_target_profile=False, provides_usage_forecast=True, fill_level_range=NumberRange(start_of_range=8670.277473912942, end_of_range=27152.584459033194)))

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_system_description = FRBCSystemDescription(message_type=FRBC.SystemDescription, message_id=uuid.UUID("a2dfaa9c-e52c-435d-94e4-15007f208ec6"), valid_from=datetime(year=2021, month=7, day=13, hour=15, minute=48, second=7, tzinfo=offset(offset=timedelta(seconds=0.0))), actuators=[FRBCActuatorDescription(id=uuid.UUID("b6872218-3fb7-436e-bdcb-e393f8ef95f7"), diagnostic_label="some-test-string6489", supported_commodities=[Commodity.GAS], operation_modes=[FRBCOperationMode(id=uuid.UUID("052029e8-85e2-4b96-bd03-7f3345445e76"), diagnostic_label="some-test-string7949", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=17740.22962461282, end_of_range=52507.59091283206), fill_rate=NumberRange(start_of_range=35532.15914996989, end_of_range=48265.232076205815), power_ranges=[PowerRange(start_of_range=38748.50842724231, end_of_range=47741.69817105044, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=35692.82350352573, end_of_range=47884.66649499221))], abnormal_condition_only=True)], transitions=[Transition(id=uuid.UUID("b1ace854-611e-4064-8c9b-434b453879df"), from_=uuid.UUID("66c5b0af-36e0-425d-b5c3-9cf27944f555"), to=uuid.UUID("8aed333c-663c-4502-8dc2-45c21acbe366"), start_timers=[uuid.UUID("56258c00-182b-4299-b9f0-c44d533dfdcb")], blocking_timers=[uuid.UUID("8dac5674-4428-46cd-bfad-c89bb4d23029")], transition_costs=1403.4899643577787, transition_duration=Duration.from_timedelta(timedelta(milliseconds=32794)), abnormal_condition_only=False)], timers=[Timer(id=uuid.UUID("e8a806df-eb45-4ed6-959d-db717d2462c8"), diagnostic_label="some-test-string3261", duration=Duration.from_timedelta(timedelta(milliseconds=5659)))])], storage=FRBCStorageDescription(diagnostic_label="some-test-string9735", fill_level_label="some-test-string1238", provides_leakage_behaviour=True, provides_fill_level_target_profile=False, provides_usage_forecast=True, fill_level_range=NumberRange(start_of_range=8670.277473912942, end_of_range=27152.584459033194)))

        # Act
        json_str = frbc_system_description.to_json()

        # Assert
        expected_json = {   'actuators': [   {   'diagnostic_label': 'some-test-string6489',
                         'id': 'b6872218-3fb7-436e-bdcb-e393f8ef95f7',
                         'operation_modes': [   {   'abnormal_condition_only': True,
                                                    'diagnostic_label': 'some-test-string7949',
                                                    'elements': [   {   'fill_level_range': {   'end_of_range': 52507.59091283206,
                                                                                                'start_of_range': 17740.22962461282},
                                                                        'fill_rate': {   'end_of_range': 48265.232076205815,
                                                                                         'start_of_range': 35532.15914996989},
                                                                        'power_ranges': [   {   'commodity_quantity': 'ELECTRIC.POWER.L1',
                                                                                                'end_of_range': 47741.69817105044,
                                                                                                'start_of_range': 38748.50842724231}],
                                                                        'running_costs': {   'end_of_range': 47884.66649499221,
                                                                                             'start_of_range': 35692.82350352573}}],
                                                    'id': '052029e8-85e2-4b96-bd03-7f3345445e76'}],
                         'supported_commodities': ['GAS'],
                         'timers': [   {   'diagnostic_label': 'some-test-string3261',
                                           'duration': 5659,
                                           'id': 'e8a806df-eb45-4ed6-959d-db717d2462c8'}],
                         'transitions': [   {   'abnormal_condition_only': False,
                                                'blocking_timers': [   '8dac5674-4428-46cd-bfad-c89bb4d23029'],
                                                'from_': '66c5b0af-36e0-425d-b5c3-9cf27944f555',
                                                'id': 'b1ace854-611e-4064-8c9b-434b453879df',
                                                'start_timers': [   '56258c00-182b-4299-b9f0-c44d533dfdcb'],
                                                'to': '8aed333c-663c-4502-8dc2-45c21acbe366',
                                                'transition_costs': 1403.4899643577787,
                                                'transition_duration': 32794}]}],
    'message_id': 'a2dfaa9c-e52c-435d-94e4-15007f208ec6',
    'message_type': 'FRBC.SystemDescription',
    'storage': {   'diagnostic_label': 'some-test-string9735',
                   'fill_level_label': 'some-test-string1238',
                   'fill_level_range': {   'end_of_range': 27152.584459033194,
                                           'start_of_range': 8670.277473912942},
                   'provides_fill_level_target_profile': False,
                   'provides_leakage_behaviour': True,
                   'provides_usage_forecast': True},
    'valid_from': '2021-07-13T15:48:07+00:00'}
        self.assertEqual(json.loads(json_str), expected_json)
