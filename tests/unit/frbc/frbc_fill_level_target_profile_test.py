
from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCFillLevelTargetProfileTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "message_type": "FRBC.FillLevelTargetProfile",
    "message_id": "8df9b5ac-de60-402c-9400-a4dd731fbd99",
    "start_time": "2023-02-12T11:42:28+11:00",
    "elements": [
        {
            "duration": 26527,
            "fill_level_range": {
                "start_of_range": 4668.6876987963915,
                "end_of_range": 25463.75618862868
            }
        }
    ]
}
        """

        # Act
        frbc_fill_level_target_profile = FRBCFillLevelTargetProfile.from_json(json_str)

        # Assert
        self.assertEqual(frbc_fill_level_target_profile.message_type, FRBC.FillLevelTargetProfile)
        self.assertEqual(frbc_fill_level_target_profile.message_id, uuid.UUID("8df9b5ac-de60-402c-9400-a4dd731fbd99"))
        self.assertEqual(frbc_fill_level_target_profile.start_time, datetime(year=2023, month=2, day=12, hour=11, minute=42, second=28, tzinfo=offset(offset=timedelta(seconds=39600.0))))
        self.assertEqual(frbc_fill_level_target_profile.elements, [FRBCFillLevelTargetProfileElement(duration=Duration.from_timedelta(timedelta(milliseconds=26527)), fill_level_range=NumberRange(start_of_range=4668.6876987963915, end_of_range=25463.75618862868))])

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_fill_level_target_profile = FRBCFillLevelTargetProfile(message_type=FRBC.FillLevelTargetProfile, message_id=uuid.UUID("8df9b5ac-de60-402c-9400-a4dd731fbd99"), start_time=datetime(year=2023, month=2, day=12, hour=11, minute=42, second=28, tzinfo=offset(offset=timedelta(seconds=39600.0))), elements=[FRBCFillLevelTargetProfileElement(duration=Duration.from_timedelta(timedelta(milliseconds=26527)), fill_level_range=NumberRange(start_of_range=4668.6876987963915, end_of_range=25463.75618862868))])

        # Act
        json_str = frbc_fill_level_target_profile.to_json()

        # Assert
        expected_json = {   'elements': [   {   'duration': 26527,
                        'fill_level_range': {   'end_of_range': 25463.75618862868,
                                                'start_of_range': 4668.6876987963915}}],
    'message_id': '8df9b5ac-de60-402c-9400-a4dd731fbd99',
    'message_type': 'FRBC.FillLevelTargetProfile',
    'start_time': '2023-02-12T11:42:28+11:00'}
        self.assertEqual(json.loads(json_str), expected_json)
