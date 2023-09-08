from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCUsageForecastTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "elements": [
        {
            "duration": 14010,
            "usage_rate_expected": 8032.572599815139,
            "usage_rate_lower_68PPR": 3910.197692207213,
            "usage_rate_lower_95PPR": 6541.633895752248,
            "usage_rate_lower_limit": 3419.1709124422173,
            "usage_rate_upper_68PPR": 7146.0702352976305,
            "usage_rate_upper_95PPR": 627.7040858037238,
            "usage_rate_upper_limit": 8477.800850190179
        }
    ],
    "message_id": "4a91b4ab-21fb-42ae-b97d-6170f8b922cc",
    "message_type": "FRBC.UsageForecast",
    "start_time": "2023-03-25T13:48:35+02:00"
}
        """

        # Act
        frbc_usage_forecast = FRBCUsageForecast.from_json(json_str)

        # Assert
        self.assertEqual(
            frbc_usage_forecast.elements,
            [
                FRBCUsageForecastElement(
                    duration=Duration.from_timedelta(timedelta(milliseconds=14010)),
                    usage_rate_expected=8032.572599815139,
                    usage_rate_lower_68PPR=3910.197692207213,
                    usage_rate_lower_95PPR=6541.633895752248,
                    usage_rate_lower_limit=3419.1709124422173,
                    usage_rate_upper_68PPR=7146.0702352976305,
                    usage_rate_upper_95PPR=627.7040858037238,
                    usage_rate_upper_limit=8477.800850190179,
                )
            ],
        )
        self.assertEqual(
            frbc_usage_forecast.message_id,
            uuid.UUID("4a91b4ab-21fb-42ae-b97d-6170f8b922cc"),
        )
        self.assertEqual(frbc_usage_forecast.message_type, "FRBC.UsageForecast")
        self.assertEqual(
            frbc_usage_forecast.start_time,
            datetime(
                year=2023,
                month=3,
                day=25,
                hour=13,
                minute=48,
                second=35,
                tzinfo=offset(offset=timedelta(seconds=7200.0)),
            ),
        )

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_usage_forecast = FRBCUsageForecast(
            elements=[
                FRBCUsageForecastElement(
                    duration=Duration.from_timedelta(timedelta(milliseconds=14010)),
                    usage_rate_expected=8032.572599815139,
                    usage_rate_lower_68PPR=3910.197692207213,
                    usage_rate_lower_95PPR=6541.633895752248,
                    usage_rate_lower_limit=3419.1709124422173,
                    usage_rate_upper_68PPR=7146.0702352976305,
                    usage_rate_upper_95PPR=627.7040858037238,
                    usage_rate_upper_limit=8477.800850190179,
                )
            ],
            message_id=uuid.UUID("4a91b4ab-21fb-42ae-b97d-6170f8b922cc"),
            message_type="FRBC.UsageForecast",
            start_time=datetime(
                year=2023,
                month=3,
                day=25,
                hour=13,
                minute=48,
                second=35,
                tzinfo=offset(offset=timedelta(seconds=7200.0)),
            ),
        )

        # Act
        json_str = frbc_usage_forecast.to_json()

        # Assert
        expected_json = {
            "elements": [
                {
                    "duration": 14010,
                    "usage_rate_expected": 8032.572599815139,
                    "usage_rate_lower_68PPR": 3910.197692207213,
                    "usage_rate_lower_95PPR": 6541.633895752248,
                    "usage_rate_lower_limit": 3419.1709124422173,
                    "usage_rate_upper_68PPR": 7146.0702352976305,
                    "usage_rate_upper_95PPR": 627.7040858037238,
                    "usage_rate_upper_limit": 8477.800850190179,
                }
            ],
            "message_id": "4a91b4ab-21fb-42ae-b97d-6170f8b922cc",
            "message_type": "FRBC.UsageForecast",
            "start_time": "2023-03-25T13:48:35+02:00",
        }
        self.assertEqual(json.loads(json_str), expected_json)
