import json
import uuid
from unittest import TestCase

from s2python.common import RevokeObject, RevokableObjects


class RevokeObjectTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """{
            "message_id": "3bdec96b-be3b-4ba9-afa0-c4a0632cced5",
            "message_type": "RevokeObject",
            "object_id": "3bdec96b-be3b-4ba9-afa0-c4a0632cced6",
            "object_type": "FRBC.Instruction"
        }
        """

        # Act
        revoke_object: RevokeObject = RevokeObject.from_json(json_str)

        # Assert
        self.assertEqual(
            revoke_object.message_id, uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632cced5")
        )
        self.assertEqual(
            revoke_object.object_id, uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632cced6")
        )
        self.assertEqual(revoke_object.object_type, RevokableObjects.FRBC_Instruction)

    def test__to_json__happy_path(self):
        # Arrange
        revoke_object = RevokeObject(
            message_id=uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632cced5"),
            object_id=uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632cced6"),
            object_type=RevokableObjects.FRBC_Instruction,
        )

        # Act
        json_str = revoke_object.to_json()

        # Assert
        expected_json = {
            "message_id": "3bdec96b-be3b-4ba9-afa0-c4a0632cced5",
            "message_type": "RevokeObject",
            "object_id": "3bdec96b-be3b-4ba9-afa0-c4a0632cced6",
            "object_type": "FRBC.Instruction",
        }
        self.assertEqual(json.loads(json_str), expected_json)
