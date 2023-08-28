from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCFillLevelTargetProfileElementTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "duration": 12950,
    "fill_level_range": {
        "end_of_range": 8176,
        "start_of_range": 6207
    }
}
        """

        # Act
        frbc_fill_level_target_profile_element = FRBCFillLevelTargetProfileElement.from_json(json_str)

        # Assert
        self.assertEqual(frbc_fill_level_target_profile_element.duration,
                         Duration.from_timedelta(timedelta(milliseconds=12950)))
        self.assertEqual(frbc_fill_level_target_profile_element.fill_level_range,
                         NumberRange(end_of_range=8176.0, start_of_range=6207.0))

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_fill_level_target_profile_element = FRBCFillLevelTargetProfileElement(
            duration=Duration.from_timedelta(timedelta(milliseconds=12950)),
            fill_level_range=NumberRange(end_of_range=8176, start_of_range=6207))

        # Act
        json_str = frbc_fill_level_target_profile_element.to_json()

        # Assert
        expected_json = {
            'duration': 12950,
            'fill_level_range': {
                'end_of_range': 8176,
                'start_of_range': 6207
            }
        }
        self.assertEqual(json.loads(json_str), expected_json)
