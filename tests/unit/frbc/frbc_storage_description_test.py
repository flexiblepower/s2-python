
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
    "diagnostic_label": "some-test-string7988",
    "fill_level_label": "some-test-string7290",
    "provides_leakage_behaviour": false,
    "provides_fill_level_target_profile": false,
    "provides_usage_forecast": false,
    "fill_level_range": {
        "start_of_range": 10366.413731478093,
        "end_of_range": 12149.613524580698
    }
}
        """

        # Act
        frbc_storage_description = FRBCStorageDescription.from_json(json_str)

        # Assert
        self.assertEqual(frbc_storage_description.diagnostic_label, "some-test-string7988")
        self.assertEqual(frbc_storage_description.fill_level_label, "some-test-string7290")
        self.assertEqual(frbc_storage_description.provides_leakage_behaviour, False)
        self.assertEqual(frbc_storage_description.provides_fill_level_target_profile, False)
        self.assertEqual(frbc_storage_description.provides_usage_forecast, False)
        self.assertEqual(frbc_storage_description.fill_level_range, NumberRange(start_of_range=10366.413731478093, end_of_range=12149.613524580698))

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_storage_description = FRBCStorageDescription(diagnostic_label="some-test-string7988", fill_level_label="some-test-string7290", provides_leakage_behaviour=False, provides_fill_level_target_profile=False, provides_usage_forecast=False, fill_level_range=NumberRange(start_of_range=10366.413731478093, end_of_range=12149.613524580698))

        # Act
        json_str = frbc_storage_description.to_json()

        # Assert
        expected_json = {   'diagnostic_label': 'some-test-string7988',
    'fill_level_label': 'some-test-string7290',
    'fill_level_range': {   'end_of_range': 12149.613524580698,
                            'start_of_range': 10366.413731478093},
    'provides_fill_level_target_profile': False,
    'provides_leakage_behaviour': False,
    'provides_usage_forecast': False}
        self.assertEqual(json.loads(json_str), expected_json)
