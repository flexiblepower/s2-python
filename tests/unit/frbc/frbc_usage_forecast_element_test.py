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
    "duration": 9317,
    "usage_rate_expected": 866.9362374046218,
    "usage_rate_lower_68PPR": 3496.6233093198375,
    "usage_rate_lower_95PPR": 4206.0536932975065,
    "usage_rate_lower_limit": 7353.272756502293,
    "usage_rate_upper_68PPR": 5124.8129813156465,
    "usage_rate_upper_95PPR": 264.3386978845277,
    "usage_rate_upper_limit": 4474.174577002476
}
        """

        # Act
        frbc_usage_forecast_element = FRBCUsageForecastElement.from_json(json_str)

        # Assert
        self.assertEqual(
            frbc_usage_forecast_element.duration,
            Duration.from_timedelta(timedelta(milliseconds=9317)),
        )
        self.assertEqual(
            frbc_usage_forecast_element.usage_rate_expected, 866.9362374046218
        )
        self.assertEqual(
            frbc_usage_forecast_element.usage_rate_lower_68PPR, 3496.6233093198375
        )
        self.assertEqual(
            frbc_usage_forecast_element.usage_rate_lower_95PPR, 4206.0536932975065
        )
        self.assertEqual(
            frbc_usage_forecast_element.usage_rate_lower_limit, 7353.272756502293
        )
        self.assertEqual(
            frbc_usage_forecast_element.usage_rate_upper_68PPR, 5124.8129813156465
        )
        self.assertEqual(
            frbc_usage_forecast_element.usage_rate_upper_95PPR, 264.3386978845277
        )
        self.assertEqual(
            frbc_usage_forecast_element.usage_rate_upper_limit, 4474.174577002476
        )

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_usage_forecast_element = FRBCUsageForecastElement(
            duration=Duration.from_timedelta(timedelta(milliseconds=9317)),
            usage_rate_expected=866.9362374046218,
            usage_rate_lower_68PPR=3496.6233093198375,
            usage_rate_lower_95PPR=4206.0536932975065,
            usage_rate_lower_limit=7353.272756502293,
            usage_rate_upper_68PPR=5124.8129813156465,
            usage_rate_upper_95PPR=264.3386978845277,
            usage_rate_upper_limit=4474.174577002476,
        )

        # Act
        json_str = frbc_usage_forecast_element.to_json()

        # Assert
        expected_json = {
            "duration": 9317,
            "usage_rate_expected": 866.9362374046218,
            "usage_rate_lower_68PPR": 3496.6233093198375,
            "usage_rate_lower_95PPR": 4206.0536932975065,
            "usage_rate_lower_limit": 7353.272756502293,
            "usage_rate_upper_68PPR": 5124.8129813156465,
            "usage_rate_upper_95PPR": 264.3386978845277,
            "usage_rate_upper_limit": 4474.174577002476,
        }
        self.assertEqual(json.loads(json_str), expected_json)
