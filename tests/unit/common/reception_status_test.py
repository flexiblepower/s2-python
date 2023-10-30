import json
import uuid
from unittest import TestCase

from s2python.common import ReceptionStatus, ReceptionStatusValues


class ReceptionStatusTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """
        { "diagnostic_label": "blablabla",
          "message_type": "ReceptionStatus",
          "status": "TEMPORARY_ERROR",
          "subject_message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced5"
        }"""

        # Act
        reception_status: ReceptionStatus = ReceptionStatus.from_json(json_str)

        # Assert
        self.assertEqual(reception_status.diagnostic_label, "blablabla")
        self.assertEqual(reception_status.status, ReceptionStatusValues.TEMPORARY_ERROR)
        self.assertEqual(
            reception_status.subject_message_id,
            uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced5"),
        )

    def test__to_json__happy_path(self):
        # Arrange
        reception_status = ReceptionStatus(
            diagnostic_label="Dagobert Duck is king!",
            message_type="ReceptionStatus",
            status=ReceptionStatusValues.OK,
            subject_message_id=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced5"),
        )

        # Act
        json_str = reception_status.to_json()

        # Assert
        expected_json = {
            "diagnostic_label": "Dagobert Duck is king!",
            "message_type": "ReceptionStatus",
            "status": "OK",
            "subject_message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced5",
        }
        self.assertEqual(json.loads(json_str), expected_json)
