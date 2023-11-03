from unittest import TestCase
from uuid import UUID

from s2python.common import HandshakeResponse
from s2python.generated.gen_s2 import EnergyManagementRole
from s2python.s2_parser import S2Parser
from s2python.common.handshake import Handshake
from s2python.s2_validation_error import S2ValidationError


class S2ParserTest(TestCase):
    def test_parse_as_any_message__str(self):
        # Arrange
        message_json = (
            '{"message_id": "ca093515-0bb3-4709-bd56-092c1808b791", "message_type": "Handshake", "role": '
            '"CEM", "supported_protocol_versions": ["3.0alpha"]}'
        )

        # Act
        parsed_message = S2Parser.parse_as_any_message(message_json)

        # Assert
        self.assertEqual(
            parsed_message,
            Handshake(
                message_id=UUID("ca093515-0bb3-4709-bd56-092c1808b791"),
                role=EnergyManagementRole.CEM,
                supported_protocol_versions=["3.0alpha"],
            ),
        )

    def test_parse_as_any_message__dict(self):
        # Arrange
        message_json = {
            "message_id": "ca093515-0bb3-4709-bd56-092c1808b791",
            "message_type": "Handshake",
            "role": "CEM",
            "supported_protocol_versions": ["3.0alpha"],
        }

        # Act
        parsed_message = S2Parser.parse_as_any_message(message_json)

        # Assert
        self.assertEqual(
            parsed_message,
            Handshake(
                message_id=UUID("ca093515-0bb3-4709-bd56-092c1808b791"),
                role=EnergyManagementRole.CEM,
                supported_protocol_versions=["3.0alpha"],
            ),
        )

    def test_parse_as_any_message__dict_validation_error(self):
        # Arrange
        message_json = {
            # "message_id": "ca093515-0bb3-4709-bd56-092c1808b791",
            "message_type": "Handshake",
            "role": "CEM",
            "supported_protocol_versions": ["3.0alpha"],
        }

        # Act / Assert
        with self.assertRaises(S2ValidationError):
            S2Parser.parse_as_any_message(message_json)

    def test_parse_as_message__str(self):
        # Arrange
        message_json = (
            '{"message_id": "ca093515-0bb3-4709-bd56-092c1808b791", "message_type": "Handshake", "role": '
            '"CEM", "supported_protocol_versions": ["3.0alpha"]}'
        )

        # Act
        parsed_message = S2Parser.parse_as_message(message_json, Handshake)

        # Assert
        self.assertEqual(
            parsed_message,
            Handshake(
                message_id=UUID("ca093515-0bb3-4709-bd56-092c1808b791"),
                role=EnergyManagementRole.CEM,
                supported_protocol_versions=["3.0alpha"],
            ),
        )

    def test_parse_as_message__dict(self):
        # Arrange
        message_json = {
            "message_id": "ca093515-0bb3-4709-bd56-092c1808b791",
            "message_type": "Handshake",
            "role": "CEM",
            "supported_protocol_versions": ["3.0alpha"],
        }

        # Act
        parsed_message = S2Parser.parse_as_message(message_json, Handshake)

        # Assert
        self.assertEqual(
            parsed_message,
            Handshake(
                message_id=UUID("ca093515-0bb3-4709-bd56-092c1808b791"),
                role=EnergyManagementRole.CEM,
                supported_protocol_versions=["3.0alpha"],
            ),
        )

    def test_parse_as_message__dict_wrong_class(self):
        # Arrange
        message_json = {
            "message_id": "ca093515-0bb3-4709-bd56-092c1808b791",
            "message_type": "Handshake",
            "role": "CEM",
            "supported_protocol_versions": ["3.0alpha"],
        }

        # Act / Assert
        with self.assertRaises(S2ValidationError):
            S2Parser.parse_as_message(message_json, HandshakeResponse)
