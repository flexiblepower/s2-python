from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCStorageDescriptionTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "diagnostic_label": "some-test-string3063",
    "fill_level_label": "some-test-string2323",
    "fill_level_range": {
        "end_of_range": 14555.806367871957,
        "start_of_range": 10409.397377840089
    },
    "provides_fill_level_target_profile": true,
    "provides_leakage_behaviour": false,
    "provides_usage_forecast": false
}
        """

        # Act
        frbc_storage_description = FRBCStorageDescription.from_json(json_str)

        # Assert
        self.assertEqual(
            frbc_storage_description.diagnostic_label, "some-test-string3063"
        )
        self.assertEqual(
            frbc_storage_description.fill_level_label, "some-test-string2323"
        )
        self.assertEqual(
            frbc_storage_description.fill_level_range,
            NumberRange(
                end_of_range=14555.806367871957, start_of_range=10409.397377840089
            ),
        )
        self.assertEqual(
            frbc_storage_description.provides_fill_level_target_profile, True
        )
        self.assertEqual(frbc_storage_description.provides_leakage_behaviour, False)
        self.assertEqual(frbc_storage_description.provides_usage_forecast, False)

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_storage_description = FRBCStorageDescription(
            diagnostic_label="some-test-string3063",
            fill_level_label="some-test-string2323",
            fill_level_range=NumberRange(
                end_of_range=14555.806367871957, start_of_range=10409.397377840089
            ),
            provides_fill_level_target_profile=True,
            provides_leakage_behaviour=False,
            provides_usage_forecast=False,
        )

        # Act
        json_str = frbc_storage_description.to_json()

        # Assert
        expected_json = {
            "diagnostic_label": "some-test-string3063",
            "fill_level_label": "some-test-string2323",
            "fill_level_range": {
                "end_of_range": 14555.806367871957,
                "start_of_range": 10409.397377840089,
            },
            "provides_fill_level_target_profile": True,
            "provides_leakage_behaviour": False,
            "provides_usage_forecast": False,
        }
        self.assertEqual(json.loads(json_str), expected_json)
