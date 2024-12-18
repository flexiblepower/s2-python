
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
    "diagnostic_label": "some-test-string6024",
    "fill_level_label": "some-test-string4194",
    "provides_leakage_behaviour": true,
    "provides_fill_level_target_profile": true,
    "provides_usage_forecast": false,
    "fill_level_range": {
        "start_of_range": 4284.806107128117,
        "end_of_range": 15952.434979774753
    }
}
        """

        # Act
        frbc_storage_description = FRBCStorageDescription.from_json(json_str)

        # Assert
        self.assertEqual(frbc_storage_description.diagnostic_label, "some-test-string6024")
        self.assertEqual(frbc_storage_description.fill_level_label, "some-test-string4194")
        self.assertEqual(frbc_storage_description.provides_leakage_behaviour, True)
        self.assertEqual(frbc_storage_description.provides_fill_level_target_profile, True)
        self.assertEqual(frbc_storage_description.provides_usage_forecast, False)
        self.assertEqual(frbc_storage_description.fill_level_range, NumberRange(start_of_range=4284.806107128117, end_of_range=15952.434979774753))

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_storage_description = FRBCStorageDescription(diagnostic_label="some-test-string6024", fill_level_label="some-test-string4194", provides_leakage_behaviour=True, provides_fill_level_target_profile=True, provides_usage_forecast=False, fill_level_range=NumberRange(start_of_range=4284.806107128117, end_of_range=15952.434979774753))

        # Act
        json_str = frbc_storage_description.to_json()

        # Assert
        expected_json = {   'diagnostic_label': 'some-test-string6024',
    'fill_level_label': 'some-test-string4194',
    'fill_level_range': {   'end_of_range': 15952.434979774753,
                            'start_of_range': 4284.806107128117},
    'provides_fill_level_target_profile': True,
    'provides_leakage_behaviour': True,
    'provides_usage_forecast': False}
        self.assertEqual(json.loads(json_str), expected_json)
