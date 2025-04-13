import json
import uuid
from unittest import TestCase

from s2python.common import SelectControlType, ControlType


class SelectControlTypeTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """{
            "control_type": "OPERATION_MODE_BASED_CONTROL",
            "message_id": "3bdec96b-be3b-4ba9-afa0-c4a0632cced5",
            "message_type": "SelectControlType"
        }"""

        # Act
        select_control_type: SelectControlType = SelectControlType.from_json(json_str)

        # Assert
        self.assertEqual(
            select_control_type.message_id,
            uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632cced5"),
        )
        self.assertEqual(select_control_type.control_type, ControlType.OPERATION_MODE_BASED_CONTROL)

    def test__to_json__happy_path(self):
        # Arrange
        select_control_type = SelectControlType(
            message_id=uuid.UUID("3bdec96b-be3b-4ba9-afa1-c4a0632cced5"),
            control_type=ControlType.DEMAND_DRIVEN_BASED_CONTROL,
        )

        # Act
        json_str = select_control_type.to_json()

        # Assert
        expected_json = {
            "control_type": "DEMAND_DRIVEN_BASED_CONTROL",
            "message_id": "3bdec96b-be3b-4ba9-afa1-c4a0632cced5",
            "message_type": "SelectControlType",
        }
        self.assertEqual(json.loads(json_str), expected_json)
