
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
    "message_id": "698ea780-c918-4ea8-aef2-885a5c0228ad",
    "start_time": "2020-05-16T18:38:12+08:00",
    "elements": [
        {
            "duration": 30067,
            "fill_level_range": {
                "start_of_range": 18107.25728114559,
                "end_of_range": 51078.86550304321
            }
        }
    ]
}
        """

        # Act
        frbc_fill_level_target_profile = FRBCFillLevelTargetProfile.from_json(json_str)

        # Assert
        self.assertEqual(frbc_fill_level_target_profile.message_type, FRBC.FillLevelTargetProfile)
        self.assertEqual(frbc_fill_level_target_profile.message_id, uuid.UUID("698ea780-c918-4ea8-aef2-885a5c0228ad"))
        self.assertEqual(frbc_fill_level_target_profile.start_time, datetime(year=2020, month=5, day=16, hour=18, minute=38, second=12, tzinfo=offset(offset=timedelta(seconds=28800.0))))
        self.assertEqual(frbc_fill_level_target_profile.elements, [FRBCFillLevelTargetProfileElement(duration=Duration.from_timedelta(timedelta(milliseconds=30067)), fill_level_range=NumberRange(start_of_range=18107.25728114559, end_of_range=51078.86550304321))])

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_fill_level_target_profile = FRBCFillLevelTargetProfile(message_type=FRBC.FillLevelTargetProfile, message_id=uuid.UUID("698ea780-c918-4ea8-aef2-885a5c0228ad"), start_time=datetime(year=2020, month=5, day=16, hour=18, minute=38, second=12, tzinfo=offset(offset=timedelta(seconds=28800.0))), elements=[FRBCFillLevelTargetProfileElement(duration=Duration.from_timedelta(timedelta(milliseconds=30067)), fill_level_range=NumberRange(start_of_range=18107.25728114559, end_of_range=51078.86550304321))])

        # Act
        json_str = frbc_fill_level_target_profile.to_json()

        # Assert
        expected_json = {   'elements': [   {   'duration': 30067,
                        'fill_level_range': {   'end_of_range': 51078.86550304321,
                                                'start_of_range': 18107.25728114559}}],
    'message_id': '698ea780-c918-4ea8-aef2-885a5c0228ad',
    'message_type': 'FRBC.FillLevelTargetProfile',
    'start_time': '2020-05-16T18:38:12+08:00'}
        self.assertEqual(json.loads(json_str), expected_json)
