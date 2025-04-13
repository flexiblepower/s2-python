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
    "elements": [
        {
            "duration": 4704,
            "fill_level_range": {
                "end_of_range": 10800.98606857073545,
                "start_of_range": 6891.19014440217
            }
        }
    ],
    "message_id": "04a6c8af-ca8d-420c-9c11-e96a70fe82b1",
    "message_type": "FRBC.FillLevelTargetProfile",
    "start_time": "2021-04-17T00:19:20Z"
}
        """

        # Act
        frbc_fill_level_target_profile = FRBCFillLevelTargetProfile.from_json(json_str)

        # Assert
        self.assertEqual(
            frbc_fill_level_target_profile.elements,
            [
                FRBCFillLevelTargetProfileElement(
                    duration=Duration.from_timedelta(timedelta(milliseconds=4704)),
                    fill_level_range=NumberRange(
                        end_of_range=10800.98606857073545,
                        start_of_range=6891.19014440217,
                    ),
                )
            ],
        )
        self.assertEqual(
            frbc_fill_level_target_profile.message_id,
            uuid.UUID("04a6c8af-ca8d-420c-9c11-e96a70fe82b1"),
        )
        self.assertEqual(
            frbc_fill_level_target_profile.message_type, "FRBC.FillLevelTargetProfile"
        )
        self.assertEqual(
            frbc_fill_level_target_profile.start_time,
            datetime(
                year=2021,
                month=4,
                day=17,
                hour=0,
                minute=19,
                second=20,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
        )

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_fill_level_target_profile = FRBCFillLevelTargetProfile(
            elements=[
                FRBCFillLevelTargetProfileElement(
                    duration=Duration.from_timedelta(timedelta(milliseconds=4704)),
                    fill_level_range=NumberRange(
                        end_of_range=10800.98606857073545,
                        start_of_range=6891.19014440217,
                    ),
                )
            ],
            message_id=uuid.UUID("04a6c8af-ca8d-420c-9c11-e96a70fe82b1"),
            message_type="FRBC.FillLevelTargetProfile",
            start_time=datetime(
                year=2021,
                month=4,
                day=17,
                hour=0,
                minute=19,
                second=20,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
        )

        # Act
        json_str = frbc_fill_level_target_profile.to_json()

        # Assert
        expected_json = {
            "elements": [
                {
                    "duration": 4704,
                    "fill_level_range": {
                        "end_of_range": 10800.98606857073545,
                        "start_of_range": 6891.19014440217,
                    },
                }
            ],
            "message_id": "04a6c8af-ca8d-420c-9c11-e96a70fe82b1",
            "message_type": "FRBC.FillLevelTargetProfile",
            "start_time": "2021-04-17T00:19:20Z",
        }
        self.assertEqual(json.loads(json_str), expected_json)
