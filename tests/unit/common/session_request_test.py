import json
import uuid
from unittest import TestCase

from s2python.common import SessionRequest, SessionRequestType


class SessionRequestTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """{
            "request": "TERMINATE",
            "message_id": "3bdec96b-be3b-4ba9-afa0-c4a0632cced5",
            "message_type": "SessionRequest"
        }"""

        # Act
        session_request: SessionRequest = SessionRequest.from_json(json_str)

        # Assert
        self.assertEqual(
            session_request.message_id,
            uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632cced5"),
        )
        self.assertEqual(session_request.request, SessionRequestType.TERMINATE)

    def test__to_json__happy_path(self):
        # Arrange
        session_request = SessionRequest(  # pyright: ignore[reportCallIssue]
            message_id=uuid.UUID("3bdec96e-be3b-4ba9-afa0-c4a0632cced5"),
            request=SessionRequestType.RECONNECT,
        )

        # Act
        json_str = session_request.to_json()

        # Assert
        expected_json = {
            "request": "RECONNECT",
            "message_id": "3bdec96e-be3b-4ba9-afa0-c4a0632cced5",
            "message_type": "SessionRequest",
        }
        self.assertEqual(json.loads(json_str), expected_json)
