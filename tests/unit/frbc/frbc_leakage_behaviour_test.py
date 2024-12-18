
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
    "message_id": "f681fa18-589b-4081-a85b-cdb608795248",
    "valid_from": "2023-09-26T17:14:46+13:00",
    "elements": [
        {
            "fill_level_range": {
                "start_of_range": 5349.224337716178,
                "end_of_range": 26642.603531976765
            },
            "leakage_rate": 3062.489155126407
        }
    ]
}
        """

        # Act
        frbc_leakage_behaviour = FRBCLeakageBehaviour.from_json(json_str)

        # Assert
        self.assertEqual(frbc_leakage_behaviour.message_type, FRBC.LeakageBehaviour)
        self.assertEqual(frbc_leakage_behaviour.message_id, uuid.UUID("f681fa18-589b-4081-a85b-cdb608795248"))
        self.assertEqual(frbc_leakage_behaviour.valid_from, datetime(year=2023, month=9, day=26, hour=17, minute=14, second=46, tzinfo=offset(offset=timedelta(seconds=46800.0))))
        self.assertEqual(frbc_leakage_behaviour.elements, [FRBCLeakageBehaviourElement(fill_level_range=NumberRange(start_of_range=5349.224337716178, end_of_range=26642.603531976765), leakage_rate=3062.489155126407)])

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_leakage_behaviour = FRBCLeakageBehaviour(message_type=FRBC.LeakageBehaviour, message_id=uuid.UUID("f681fa18-589b-4081-a85b-cdb608795248"), valid_from=datetime(year=2023, month=9, day=26, hour=17, minute=14, second=46, tzinfo=offset(offset=timedelta(seconds=46800.0))), elements=[FRBCLeakageBehaviourElement(fill_level_range=NumberRange(start_of_range=5349.224337716178, end_of_range=26642.603531976765), leakage_rate=3062.489155126407)])

        # Act
        json_str = frbc_leakage_behaviour.to_json()

        # Assert
        expected_json = {   'elements': [   {   'fill_level_range': {   'end_of_range': 26642.603531976765,
                                                'start_of_range': 5349.224337716178},
                        'leakage_rate': 3062.489155126407}],
    'message_id': 'f681fa18-589b-4081-a85b-cdb608795248',
    'message_type': 'FRBC.LeakageBehaviour',
    'valid_from': '2023-09-26T17:14:46+13:00'}
        self.assertEqual(json.loads(json_str), expected_json)
