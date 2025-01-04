
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
    "message_type": "FRBC.StorageStatus",
    "message_id": "2b7b06cb-b4a6-4997-9d0c-8ea075f9941a",
    "present_fill_level": 226.70889257233483
}
        """

        # Act
        frbc_storage_status = FRBCStorageStatus.from_json(json_str)

        # Assert
        self.assertEqual(frbc_storage_status.message_type, FRBC.StorageStatus)
        self.assertEqual(frbc_storage_status.message_id, uuid.UUID("2b7b06cb-b4a6-4997-9d0c-8ea075f9941a"))
        self.assertEqual(frbc_storage_status.present_fill_level, 226.70889257233483)

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_storage_status = FRBCStorageStatus(message_type=FRBC.StorageStatus, message_id=uuid.UUID("2b7b06cb-b4a6-4997-9d0c-8ea075f9941a"), present_fill_level=226.70889257233483)

        # Act
        json_str = frbc_storage_status.to_json()

        # Assert
        expected_json = {   'message_id': '2b7b06cb-b4a6-4997-9d0c-8ea075f9941a',
    'message_type': 'FRBC.StorageStatus',
    'present_fill_level': 226.70889257233483}
        self.assertEqual(json.loads(json_str), expected_json)
