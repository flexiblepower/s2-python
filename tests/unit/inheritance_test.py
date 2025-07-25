import datetime
import unittest
import uuid
from typing import Optional

from pydantic import Field

from s2python.frbc import FRBCStorageStatus as FRBCStorageStatusOfficial
from s2python.s2_validation_error import S2ValidationError


class FRBCStorageStatus(FRBCStorageStatusOfficial):
    measurement_timestamp: Optional[datetime.datetime] = Field(
        default=None, description="Timestamp when fill level was measured."
    )


class InheritanceTest(unittest.TestCase):
    def test__inheritance__init(self):
        # Arrange / Act
        frbc_storage_status = FRBCStorageStatus(message_id=uuid.uuid4(),
                                                present_fill_level=0.0,
                                                measurement_timestamp=None)

        # Assert
        self.assertIsInstance(frbc_storage_status, FRBCStorageStatus)
        self.assertIsNone(frbc_storage_status.measurement_timestamp)

    def test__inheritance__init_wrong(self):
        # Arrange / Act / Assert
        with self.assertRaises(S2ValidationError):
            FRBCStorageStatus(message_id=uuid.uuid4(),
                              present_fill_level=0.0,
                              measurement_timestamp=False)  # pyright: ignore [reportArgumentType]

    def test__inheritance__from_json(self):
        # Arrange
        json_str = """
        {
        "message_id": "6bad8186-9ebf-4647-ac45-1c6856511a2f",
        "message_type": "FRBC.StorageStatus",
        "present_fill_level": 2443.939298819414,
        "measurement_timestamp": "2025-01-01T00:00:00Z"
        }"""

        # Act
        frbc_storage_status = FRBCStorageStatus.from_json(json_str)

        # Assert
        self.assertIsInstance(frbc_storage_status, FRBCStorageStatus)
        self.assertEqual(frbc_storage_status.measurement_timestamp, datetime.datetime.fromisoformat("2025-01-01T00:00:00+00:00"))
