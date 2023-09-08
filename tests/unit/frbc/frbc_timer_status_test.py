from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCTimerStatusTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "actuator_id": "f2e1f540-0235-429f-a45c-4d5cbe65d33f",
    "finished_at": "2020-11-03T12:57:27+02:00",
    "message_id": "57240f00-0b91-49bb-a4b0-2107d062faec",
    "message_type": "FRBC.TimerStatus",
    "timer_id": "bcb8e64f-ea4c-4b92-b4cb-20026a13d663"
}
        """

        # Act
        frbc_timer_status = FRBCTimerStatus.from_json(json_str)

        # Assert
        self.assertEqual(
            frbc_timer_status.actuator_id,
            uuid.UUID("f2e1f540-0235-429f-a45c-4d5cbe65d33f"),
        )
        self.assertEqual(
            frbc_timer_status.finished_at,
            datetime(
                year=2020,
                month=11,
                day=3,
                hour=12,
                minute=57,
                second=27,
                tzinfo=offset(offset=timedelta(seconds=7200.0)),
            ),
        )
        self.assertEqual(
            frbc_timer_status.message_id,
            uuid.UUID("57240f00-0b91-49bb-a4b0-2107d062faec"),
        )
        self.assertEqual(frbc_timer_status.message_type, "FRBC.TimerStatus")
        self.assertEqual(
            frbc_timer_status.timer_id,
            uuid.UUID("bcb8e64f-ea4c-4b92-b4cb-20026a13d663"),
        )

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_timer_status = FRBCTimerStatus(
            actuator_id=uuid.UUID("f2e1f540-0235-429f-a45c-4d5cbe65d33f"),
            finished_at=datetime(
                year=2020,
                month=11,
                day=3,
                hour=12,
                minute=57,
                second=27,
                tzinfo=offset(offset=timedelta(seconds=7200.0)),
            ),
            message_id=uuid.UUID("57240f00-0b91-49bb-a4b0-2107d062faec"),
            message_type="FRBC.TimerStatus",
            timer_id=uuid.UUID("bcb8e64f-ea4c-4b92-b4cb-20026a13d663"),
        )

        # Act
        json_str = frbc_timer_status.to_json()

        # Assert
        expected_json = {
            "actuator_id": "f2e1f540-0235-429f-a45c-4d5cbe65d33f",
            "finished_at": "2020-11-03T12:57:27+02:00",
            "message_id": "57240f00-0b91-49bb-a4b0-2107d062faec",
            "message_type": "FRBC.TimerStatus",
            "timer_id": "bcb8e64f-ea4c-4b92-b4cb-20026a13d663",
        }
        self.assertEqual(json.loads(json_str), expected_json)
