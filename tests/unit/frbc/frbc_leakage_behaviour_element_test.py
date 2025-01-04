
from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCLeakageBehaviourElementTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "fill_level_range": {
        "start_of_range": 13590.14671121342,
        "end_of_range": 25393.13672324905
    },
    "leakage_rate": 8822.586828251793
}
        """

        # Act
        frbc_leakage_behaviour_element = FRBCLeakageBehaviourElement.from_json(json_str)

        # Assert
        self.assertEqual(frbc_leakage_behaviour_element.fill_level_range, NumberRange(start_of_range=13590.14671121342, end_of_range=25393.13672324905))
        self.assertEqual(frbc_leakage_behaviour_element.leakage_rate, 8822.586828251793)

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_leakage_behaviour_element = FRBCLeakageBehaviourElement(fill_level_range=NumberRange(start_of_range=13590.14671121342, end_of_range=25393.13672324905), leakage_rate=8822.586828251793)

        # Act
        json_str = frbc_leakage_behaviour_element.to_json()

        # Assert
        expected_json = {   'fill_level_range': {   'end_of_range': 25393.13672324905,
                            'start_of_range': 13590.14671121342},
    'leakage_rate': 8822.586828251793}
        self.assertEqual(json.loads(json_str), expected_json)
