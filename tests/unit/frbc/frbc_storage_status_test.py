from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCStorageStatusTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "message_id": "6bad8186-9ebf-4647-ac45-1c6856511a2f",
    "message_type": "FRBC.StorageStatus",
    "present_fill_level": 2443.939298819414
}
        """

        # Act
        frbc_storage_status = FRBCStorageStatus.from_json(json_str)

        # Assert
        self.assertEqual(
            frbc_storage_status.message_id,
            uuid.UUID("6bad8186-9ebf-4647-ac45-1c6856511a2f"),
        )
        self.assertEqual(frbc_storage_status.message_type, "FRBC.StorageStatus")
        self.assertEqual(frbc_storage_status.present_fill_level, 2443.939298819414)

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_storage_status = FRBCStorageStatus(
            message_id=uuid.UUID("6bad8186-9ebf-4647-ac45-1c6856511a2f"),
            message_type="FRBC.StorageStatus",
            present_fill_level=2443.939298819414,
        )

        # Act
        json_str = frbc_storage_status.to_json()

        # Assert
        expected_json = {
            "message_id": "6bad8186-9ebf-4647-ac45-1c6856511a2f",
            "message_type": "FRBC.StorageStatus",
            "present_fill_level": 2443.939298819414,
        }
        self.assertEqual(json.loads(json_str), expected_json)
