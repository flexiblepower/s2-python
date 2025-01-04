
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
    "message_type": "FRBC.TimerStatus",
    "message_id": "b9060ff4-322c-4ec4-a1d0-1db024dd2fe7",
    "timer_id": "564ceeaa-5f4f-46f9-8986-8c7920f76c85",
    "actuator_id": "5d0523a8-2d85-417e-a83c-ddc9a6694cc2",
    "finished_at": "2021-10-18T02:07:15-02:00"
}
        """

        # Act
        frbc_timer_status = FRBCTimerStatus.from_json(json_str)

        # Assert
        self.assertEqual(frbc_timer_status.message_type, FRBC.TimerStatus)
        self.assertEqual(frbc_timer_status.message_id, uuid.UUID("b9060ff4-322c-4ec4-a1d0-1db024dd2fe7"))
        self.assertEqual(frbc_timer_status.timer_id, uuid.UUID("564ceeaa-5f4f-46f9-8986-8c7920f76c85"))
        self.assertEqual(frbc_timer_status.actuator_id, uuid.UUID("5d0523a8-2d85-417e-a83c-ddc9a6694cc2"))
        self.assertEqual(frbc_timer_status.finished_at, datetime(year=2021, month=10, day=18, hour=2, minute=7, second=15, tzinfo=offset(offset=timedelta(seconds=-7200.0))))

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_timer_status = FRBCTimerStatus(message_type=FRBC.TimerStatus, message_id=uuid.UUID("b9060ff4-322c-4ec4-a1d0-1db024dd2fe7"), timer_id=uuid.UUID("564ceeaa-5f4f-46f9-8986-8c7920f76c85"), actuator_id=uuid.UUID("5d0523a8-2d85-417e-a83c-ddc9a6694cc2"), finished_at=datetime(year=2021, month=10, day=18, hour=2, minute=7, second=15, tzinfo=offset(offset=timedelta(seconds=-7200.0))))

        # Act
        json_str = frbc_timer_status.to_json()

        # Assert
        expected_json = {   'actuator_id': '5d0523a8-2d85-417e-a83c-ddc9a6694cc2',
    'finished_at': '2021-10-18T02:07:15-02:00',
    'message_id': 'b9060ff4-322c-4ec4-a1d0-1db024dd2fe7',
    'message_type': 'FRBC.TimerStatus',
    'timer_id': '564ceeaa-5f4f-46f9-8986-8c7920f76c85'}
        self.assertEqual(json.loads(json_str), expected_json)
