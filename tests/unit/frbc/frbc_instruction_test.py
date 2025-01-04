from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCInstructionTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "abnormal_condition": true,
    "actuator_id": "db7855dd-05c4-4ba8-81e2-d10001c5bc3f",
    "execution_time": "2023-04-11T16:46:33+01:00",
    "id": "9ffd68cd-b0e2-44a6-aded-4dce6c18247e",
    "message_id": "bcb3e1da-e797-4951-86be-5e5d9136c63f",
    "message_type": "FRBC.Instruction",
    "operation_mode": "e7bf29a7-4ebc-49c1-a1fb-20725f450c91",
    "operation_mode_factor": 2303.58902271682
}
        """

        # Act
        frbc_instruction = FRBCInstruction.from_json(json_str)

        # Assert
        self.assertEqual(frbc_instruction.abnormal_condition, True)
        self.assertEqual(
            frbc_instruction.actuator_id,
            uuid.UUID("db7855dd-05c4-4ba8-81e2-d10001c5bc3f"),
        )
        self.assertEqual(
            frbc_instruction.execution_time,
            datetime(
                year=2023,
                month=4,
                day=11,
                hour=16,
                minute=46,
                second=33,
                tzinfo=offset(offset=timedelta(seconds=3600.0)),
            ),
        )
        self.assertEqual(
            frbc_instruction.id, uuid.UUID("9ffd68cd-b0e2-44a6-aded-4dce6c18247e")
        )
        self.assertEqual(
            frbc_instruction.message_id,
            uuid.UUID("bcb3e1da-e797-4951-86be-5e5d9136c63f"),
        )
        self.assertEqual(frbc_instruction.message_type, "FRBC.Instruction")
        self.assertEqual(
            frbc_instruction.operation_mode,
            uuid.UUID("e7bf29a7-4ebc-49c1-a1fb-20725f450c91"),
        )
        self.assertEqual(frbc_instruction.operation_mode_factor, 2303.58902271682)

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_instruction = FRBCInstruction(
            abnormal_condition=True,
            actuator_id=uuid.UUID("db7855dd-05c4-4ba8-81e2-d10001c5bc3f"),
            execution_time=datetime(
                year=2023,
                month=4,
                day=11,
                hour=16,
                minute=46,
                second=33,
                tzinfo=offset(offset=timedelta(seconds=3600.0)),
            ),
            id=uuid.UUID("9ffd68cd-b0e2-44a6-aded-4dce6c18247e"),
            message_id=uuid.UUID("bcb3e1da-e797-4951-86be-5e5d9136c63f"),
            message_type="FRBC.Instruction",
            operation_mode=uuid.UUID("e7bf29a7-4ebc-49c1-a1fb-20725f450c91"),
            operation_mode_factor=2303.58902271682,
        )

        # Act
        json_str = frbc_instruction.to_json()

        # Assert
        expected_json = {
            "abnormal_condition": True,
            "actuator_id": "db7855dd-05c4-4ba8-81e2-d10001c5bc3f",
            "execution_time": "2023-04-11T16:46:33+01:00",
            "id": "9ffd68cd-b0e2-44a6-aded-4dce6c18247e",
            "message_id": "bcb3e1da-e797-4951-86be-5e5d9136c63f",
            "message_type": "FRBC.Instruction",
            "operation_mode": "e7bf29a7-4ebc-49c1-a1fb-20725f450c91",
            "operation_mode_factor": 2303.58902271682,
        }
        self.assertEqual(json.loads(json_str), expected_json)
