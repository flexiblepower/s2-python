
from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCLeakageBehaviourTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "message_type": "FRBC.LeakageBehaviour",
    "message_id": "b77d33ab-1dce-4fde-859a-d22b40364c2e",
    "valid_from": "2021-09-02T00:18:01+00:00",
    "elements": [
        {
            "fill_level_range": {
                "start_of_range": 8607.996640989155,
                "end_of_range": 48389.84849678871
            },
            "leakage_rate": 8425.146853345715
        }
    ]
}
        """

        # Act
        frbc_leakage_behaviour = FRBCLeakageBehaviour.from_json(json_str)

        # Assert
        self.assertEqual(frbc_leakage_behaviour.message_type, FRBC.LeakageBehaviour)
        self.assertEqual(frbc_leakage_behaviour.message_id, uuid.UUID("b77d33ab-1dce-4fde-859a-d22b40364c2e"))
        self.assertEqual(frbc_leakage_behaviour.valid_from, datetime(year=2021, month=9, day=2, hour=0, minute=18, second=1, tzinfo=offset(offset=timedelta(seconds=0.0))))
        self.assertEqual(frbc_leakage_behaviour.elements, [FRBCLeakageBehaviourElement(fill_level_range=NumberRange(start_of_range=8607.996640989155, end_of_range=48389.84849678871), leakage_rate=8425.146853345715)])

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_leakage_behaviour = FRBCLeakageBehaviour(message_type=FRBC.LeakageBehaviour, message_id=uuid.UUID("b77d33ab-1dce-4fde-859a-d22b40364c2e"), valid_from=datetime(year=2021, month=9, day=2, hour=0, minute=18, second=1, tzinfo=offset(offset=timedelta(seconds=0.0))), elements=[FRBCLeakageBehaviourElement(fill_level_range=NumberRange(start_of_range=8607.996640989155, end_of_range=48389.84849678871), leakage_rate=8425.146853345715)])

        # Act
        json_str = frbc_leakage_behaviour.to_json()

        # Assert
        expected_json = {   'elements': [   {   'fill_level_range': {   'end_of_range': 48389.84849678871,
                                                'start_of_range': 8607.996640989155},
                        'leakage_rate': 8425.146853345715}],
    'message_id': 'b77d33ab-1dce-4fde-859a-d22b40364c2e',
    'message_type': 'FRBC.LeakageBehaviour',
    'valid_from': '2021-09-02T00:18:01+00:00'}
        self.assertEqual(json.loads(json_str), expected_json)
