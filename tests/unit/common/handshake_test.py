import json
import uuid
from unittest import TestCase

from s2python.common import Handshake, EnergyManagementRole


class HandshakeTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = (
            '{"message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3", "message_type": "Handshake", "role": "RM", '
            '"supported_protocol_versions": ["v1", "v2"]}'
        )

        # Act
        handshake = Handshake.from_json(json_str)

        # Assert
        self.assertEqual(
            handshake.message_id, uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3")
        )
        self.assertEqual(handshake.role, EnergyManagementRole.RM)
        self.assertEqual(handshake.supported_protocol_versions, ["v1", "v2"])

    def test__to_json__happy_path(self):
        # Arrange
        handshake = Handshake(
            message_id=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3"),
            role=EnergyManagementRole.CEM,
            supported_protocol_versions=["v3"],
        )

        # Act
        json_str = handshake.to_json()

        # Assert
        expected_json = {
            "message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3",
            "message_type": "Handshake",
            "role": "CEM",
            "supported_protocol_versions": ["v3"],
        }
        self.assertEqual(json.loads(json_str), expected_json)
