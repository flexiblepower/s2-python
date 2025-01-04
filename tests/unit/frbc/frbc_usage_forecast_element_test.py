
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
    "duration": 5364,
    "usage_rate_upper_limit": 2449.222540239615,
    "usage_rate_upper_95PPR": 1833.1006975798746,
    "usage_rate_upper_68PPR": 7339.63634801623,
    "usage_rate_expected": 2939.725042558339,
    "usage_rate_lower_68PPR": 4643.821202571105,
    "usage_rate_lower_95PPR": 1244.2496151489897,
    "usage_rate_lower_limit": 5214.934978137386
}
        """

        # Act
        frbc_usage_forecast_element = FRBCUsageForecastElement.from_json(json_str)

        # Assert
        self.assertEqual(frbc_usage_forecast_element.duration, Duration.from_timedelta(timedelta(milliseconds=5364)))
        self.assertEqual(frbc_usage_forecast_element.usage_rate_upper_limit, 2449.222540239615)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_upper_95PPR, 1833.1006975798746)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_upper_68PPR, 7339.63634801623)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_expected, 2939.725042558339)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_lower_68PPR, 4643.821202571105)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_lower_95PPR, 1244.2496151489897)
        self.assertEqual(frbc_usage_forecast_element.usage_rate_lower_limit, 5214.934978137386)

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_usage_forecast_element = FRBCUsageForecastElement(duration=Duration.from_timedelta(timedelta(milliseconds=5364)), usage_rate_upper_limit=2449.222540239615, usage_rate_upper_95PPR=1833.1006975798746, usage_rate_upper_68PPR=7339.63634801623, usage_rate_expected=2939.725042558339, usage_rate_lower_68PPR=4643.821202571105, usage_rate_lower_95PPR=1244.2496151489897, usage_rate_lower_limit=5214.934978137386)

        # Act
        json_str = frbc_usage_forecast_element.to_json()

        # Assert
        expected_json = {   'duration': 5364,
    'usage_rate_expected': 2939.725042558339,
    'usage_rate_lower_68PPR': 4643.821202571105,
    'usage_rate_lower_95PPR': 1244.2496151489897,
    'usage_rate_lower_limit': 5214.934978137386,
    'usage_rate_upper_68PPR': 7339.63634801623,
    'usage_rate_upper_95PPR': 1833.1006975798746,
    'usage_rate_upper_limit': 2449.222540239615}
        self.assertEqual(json.loads(json_str), expected_json)
