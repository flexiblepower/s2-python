from datetime import datetime, timezone as offset, timedelta
import json
import uuid
from unittest import TestCase

from pytz import timezone

from s2python.common import InstructionStatusUpdate, InstructionStatus


class InstructionStatusUpdateTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """{"message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3",
                       "message_type": "InstructionStatusUpdate",
                       "instruction_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced4",
                       "status_type": "SUCCEEDED",
                       "timestamp": "2023-08-02T12:48:42+01:00"}
                       """

        # Act
        instruction_status_update = InstructionStatusUpdate.from_json(json_str)

        # Assert
        self.assertEqual(
            instruction_status_update.message_id,
            uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3"),
        )
        self.assertEqual(
            instruction_status_update.instruction_id,
            uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced4"),
        )
        self.assertEqual(
            instruction_status_update.status_type, InstructionStatus.SUCCEEDED
        )
        self.assertEqual(
            instruction_status_update.timestamp,
            datetime(2023, 8, 2, 12, 48, 42, tzinfo=offset(timedelta(hours=1))),
        )

    def test__to_json__happy_path(self):
        # Arrange
        instruction_status_update = InstructionStatusUpdate(
            message_id=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3"),
            instruction_id=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced4"),
            status_type=InstructionStatus.SUCCEEDED,
            timestamp=timezone("Europe/Amsterdam").localize(
                datetime(2023, 8, 2, 12, 48, 42)
            ),
        )

        # Act
        json_str = instruction_status_update.to_json()

        # Assert
        expected_json = {
            "message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3",
            "message_type": "InstructionStatusUpdate",
            "instruction_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced4",
            "status_type": "SUCCEEDED",
            "timestamp": "2023-08-02T12:48:42+02:00",
        }
        self.assertEqual(json.loads(json_str), expected_json)
