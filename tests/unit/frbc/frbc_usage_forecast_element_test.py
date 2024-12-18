
from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCUsageForecastElementTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "duration": 3339,
    "usage_rate_upper_limit": 5657.302338158246,
    "usage_rate_upper_95PPR": 3774.615782357365,
    "usage_rate_upper_68PPR": 8333.351165894339,
    "usage_rate_expected": 8333.127007404517,
    "usage_rate_lower_68PPR": 6418.649606433992,
    "usage_rate_lower_95PPR": 3342.9603968663487,
    "usage_rate_lower_limit": 8970.532671485054
}
        """

        # Act
        frbc_usage_forecast_element = FRBCUsageForecastElement.from_json(json_str)

        # Assert
        self.assertEqual(frbc_usage_forecast_element.duration, Duration.from_timedelta(timedelta(milliseconds=3339)))
        self.assertEqual(frbc_usage_forecast_element.usage_rate_upper_limit, 5657.302338158246)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_upper_95PPR, 3774.615782357365)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_upper_68PPR, 8333.351165894339)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_expected, 8333.127007404517)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_lower_68PPR, 6418.649606433992)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_lower_95PPR, 3342.9603968663487)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_lower_limit, 8970.532671485054)

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_usage_forecast_element = FRBCUsageForecastElement(duration=Duration.from_timedelta(timedelta(milliseconds=3339)), usage_rate_upper_limit=5657.302338158246, usage_rate_upper_95PPR=3774.615782357365, usage_rate_upper_68PPR=8333.351165894339, usage_rate_expected=8333.127007404517, usage_rate_lower_68PPR=6418.649606433992, usage_rate_lower_95PPR=3342.9603968663487, usage_rate_lower_limit=8970.532671485054)

        # Act
        json_str = frbc_usage_forecast_element.to_json()

        # Assert
        expected_json = {   'duration': 3339,
    'usage_rate_expected': 8333.127007404517,
    'usage_rate_lower_68PPR': 6418.649606433992,
    'usage_rate_lower_95PPR': 3342.9603968663487,
    'usage_rate_lower_limit': 8970.532671485054,
    'usage_rate_upper_68PPR': 8333.351165894339,
    'usage_rate_upper_95PPR': 3774.615782357365,
    'usage_rate_upper_limit': 5657.302338158246}
        self.assertEqual(json.loads(json_str), expected_json)
