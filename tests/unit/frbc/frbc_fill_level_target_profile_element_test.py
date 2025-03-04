from datetime import timedelta
import json
from unittest import TestCase

from s2python.common import *
from s2python.frbc import *
from s2python.s2_validation_error import S2ValidationError


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
        frbc_fill_level_target_profile_element = (
            FRBCFillLevelTargetProfileElement.from_json(json_str)
        )

        # Assert
        self.assertEqual(
            frbc_fill_level_target_profile_element.duration,
            Duration.from_timedelta(timedelta(milliseconds=12950)),
        )
        self.assertEqual(
            frbc_fill_level_target_profile_element.fill_level_range,
            NumberRange(end_of_range=8176.0, start_of_range=6207.0),
        )

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_fill_level_target_profile_element = FRBCFillLevelTargetProfileElement(
            duration=Duration.from_timedelta(timedelta(milliseconds=12950)),
            fill_level_range=NumberRange(end_of_range=8176, start_of_range=6207),
        )

        # Act
        json_str = frbc_fill_level_target_profile_element.to_json()

        # Assert
        expected_json = {
            "duration": 12950,
            "fill_level_range": {"end_of_range": 8176, "start_of_range": 6207},
        }
        self.assertEqual(json.loads(json_str), expected_json)

    def test__init__fill_level_range_end_is_smaller_than_start(self):
        # Arrange / Act / Assert
        with self.assertRaises(S2ValidationError):
            FRBCFillLevelTargetProfileElement(
                duration=Duration.from_timedelta(timedelta(milliseconds=12950)),
                fill_level_range=NumberRange(end_of_range=6000, start_of_range=8176),
            )
