
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
    "message_id": "19c25c4f-1dd6-4a74-9e1c-54c09025844a",
    "timer_id": "329b57fb-c4e8-41f4-922f-f27eb32214d5",
    "actuator_id": "c24e5b81-0047-41db-9dba-1840c0a1aaca",
    "finished_at": "2021-08-25T09:46:58-09:00"
}
        """

        # Act
        frbc_timer_status = FRBCTimerStatus.from_json(json_str)

        # Assert
        self.assertEqual(frbc_timer_status.message_type, FRBC.TimerStatus)
        self.assertEqual(frbc_timer_status.message_id, uuid.UUID("19c25c4f-1dd6-4a74-9e1c-54c09025844a"))
        self.assertEqual(frbc_timer_status.timer_id, uuid.UUID("329b57fb-c4e8-41f4-922f-f27eb32214d5"))
        self.assertEqual(frbc_timer_status.actuator_id, uuid.UUID("c24e5b81-0047-41db-9dba-1840c0a1aaca"))
        self.assertEqual(frbc_timer_status.finished_at, datetime(year=2021, month=8, day=25, hour=9, minute=46, second=58, tzinfo=offset(offset=timedelta(seconds=-32400.0))))

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_timer_status = FRBCTimerStatus(message_type=FRBC.TimerStatus, message_id=uuid.UUID("19c25c4f-1dd6-4a74-9e1c-54c09025844a"), timer_id=uuid.UUID("329b57fb-c4e8-41f4-922f-f27eb32214d5"), actuator_id=uuid.UUID("c24e5b81-0047-41db-9dba-1840c0a1aaca"), finished_at=datetime(year=2021, month=8, day=25, hour=9, minute=46, second=58, tzinfo=offset(offset=timedelta(seconds=-32400.0))))

        # Act
        json_str = frbc_timer_status.to_json()

        # Assert
        expected_json = {   'actuator_id': 'c24e5b81-0047-41db-9dba-1840c0a1aaca',
    'finished_at': '2021-08-25T09:46:58-09:00',
    'message_id': '19c25c4f-1dd6-4a74-9e1c-54c09025844a',
    'message_type': 'FRBC.TimerStatus',
    'timer_id': '329b57fb-c4e8-41f4-922f-f27eb32214d5'}
        self.assertEqual(json.loads(json_str), expected_json)
