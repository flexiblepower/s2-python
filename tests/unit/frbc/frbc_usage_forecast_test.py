
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
    "message_type": "FRBC.UsageForecast",
    "message_id": "251e2ef9-31d5-40a0-bbf6-8331742f18ad",
    "start_time": "2021-09-09T03:50:01-01:00",
    "elements": [
        {
            "duration": 1074,
            "usage_rate_upper_limit": 3368.642281190435,
            "usage_rate_upper_95PPR": 6948.368971520732,
            "usage_rate_upper_68PPR": 1917.1869702535832,
            "usage_rate_expected": 3804.5466318560825,
            "usage_rate_lower_68PPR": 7641.102737197381,
            "usage_rate_lower_95PPR": 1017.0167039060763,
            "usage_rate_lower_limit": 1775.7219717302214
        }
    ]
}
        """

        # Act
        frbc_usage_forecast = FRBCUsageForecast.from_json(json_str)

        # Assert
        self.assertEqual(frbc_usage_forecast.message_type, FRBC.UsageForecast)
        self.assertEqual(frbc_usage_forecast.message_id, uuid.UUID("251e2ef9-31d5-40a0-bbf6-8331742f18ad"))
        self.assertEqual(frbc_usage_forecast.start_time, datetime(year=2021, month=9, day=9, hour=3, minute=50, second=1, tzinfo=offset(offset=timedelta(seconds=-3600.0))))
        self.assertEqual(frbc_usage_forecast.elements, [FRBCUsageForecastElement(duration=Duration.from_timedelta(timedelta(milliseconds=1074)), usage_rate_upper_limit=3368.642281190435, usage_rate_upper_95PPR=6948.368971520732, usage_rate_upper_68PPR=1917.1869702535832, usage_rate_expected=3804.5466318560825, usage_rate_lower_68PPR=7641.102737197381, usage_rate_lower_95PPR=1017.0167039060763, usage_rate_lower_limit=1775.7219717302214)])

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_usage_forecast = FRBCUsageForecast(message_type=FRBC.UsageForecast, message_id=uuid.UUID("251e2ef9-31d5-40a0-bbf6-8331742f18ad"), start_time=datetime(year=2021, month=9, day=9, hour=3, minute=50, second=1, tzinfo=offset(offset=timedelta(seconds=-3600.0))), elements=[FRBCUsageForecastElement(duration=Duration.from_timedelta(timedelta(milliseconds=1074)), usage_rate_upper_limit=3368.642281190435, usage_rate_upper_95PPR=6948.368971520732, usage_rate_upper_68PPR=1917.1869702535832, usage_rate_expected=3804.5466318560825, usage_rate_lower_68PPR=7641.102737197381, usage_rate_lower_95PPR=1017.0167039060763, usage_rate_lower_limit=1775.7219717302214)])

        # Act
        json_str = frbc_usage_forecast.to_json()

        # Assert
        expected_json = {   'elements': [   {   'duration': 1074,
                        'usage_rate_expected': 3804.5466318560825,
                        'usage_rate_lower_68PPR': 7641.102737197381,
                        'usage_rate_lower_95PPR': 1017.0167039060763,
                        'usage_rate_lower_limit': 1775.7219717302214,
                        'usage_rate_upper_68PPR': 1917.1869702535832,
                        'usage_rate_upper_95PPR': 6948.368971520732,
                        'usage_rate_upper_limit': 3368.642281190435}],
    'message_id': '251e2ef9-31d5-40a0-bbf6-8331742f18ad',
    'message_type': 'FRBC.UsageForecast',
    'start_time': '2021-09-09T03:50:01-01:00'}
        self.assertEqual(json.loads(json_str), expected_json)
