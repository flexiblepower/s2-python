import json
import uuid
from unittest import TestCase

from s2python.common import HandshakeResponse


class HandshakeResponseTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = (
            '{"message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3", "message_type": "HandshakeResponse", '
            '"selected_protocol_version": "v1"}'
        )

        # Act
        handshake_response: HandshakeResponse = HandshakeResponse.from_json(json_str)

        # Assert
        self.assertEqual(
            handshake_response.message_id,
            uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3"),
        )
        self.assertEqual(handshake_response.message_type, "HandshakeResponse")
        self.assertEqual(handshake_response.selected_protocol_version, "v1")

    def test__to_json__happy_path(self):
        # Arrange
        handshake_response = HandshakeResponse(
            message_id=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3"),
            selected_protocol_version="v1",
        )

        # Act
        json_str = handshake_response.to_json()

        # Assert
        expected_json = {
            "message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3",
            "message_type": "HandshakeResponse",
            "selected_protocol_version": "v1",
        }
        self.assertEqual(json.loads(json_str), expected_json)
