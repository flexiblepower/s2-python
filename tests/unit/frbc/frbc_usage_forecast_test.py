
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
    "message_id": "88f742b5-ef8e-4af9-8ae4-633922859a8e",
    "start_time": "2022-11-21T01:57:56-09:00",
    "elements": [
        {
            "duration": 8336,
            "usage_rate_upper_limit": 2600.090517037444,
            "usage_rate_upper_95PPR": 5466.368905051084,
            "usage_rate_upper_68PPR": 7874.9948212758245,
            "usage_rate_expected": 1233.4751600765392,
            "usage_rate_lower_68PPR": 1785.90944809586,
            "usage_rate_lower_95PPR": 1047.0960233716157,
            "usage_rate_lower_limit": 4680.219153555034
        }
    ]
}
        """

        # Act
        frbc_usage_forecast = FRBCUsageForecast.from_json(json_str)

        # Assert
        self.assertEqual(frbc_usage_forecast.message_type, FRBC.UsageForecast)
        self.assertEqual(frbc_usage_forecast.message_id, uuid.UUID("88f742b5-ef8e-4af9-8ae4-633922859a8e"))
        self.assertEqual(frbc_usage_forecast.start_time, datetime(year=2022, month=11, day=21, hour=1, minute=57, second=56, tzinfo=offset(offset=timedelta(seconds=-32400.0))))
        self.assertEqual(frbc_usage_forecast.elements, [FRBCUsageForecastElement(duration=Duration.from_timedelta(timedelta(milliseconds=8336)), usage_rate_upper_limit=2600.090517037444, usage_rate_upper_95PPR=5466.368905051084, usage_rate_upper_68PPR=7874.9948212758245, usage_rate_expected=1233.4751600765392, usage_rate_lower_68PPR=1785.90944809586, usage_rate_lower_95PPR=1047.0960233716157, usage_rate_lower_limit=4680.219153555034)])

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_usage_forecast = FRBCUsageForecast(message_type=FRBC.UsageForecast, message_id=uuid.UUID("88f742b5-ef8e-4af9-8ae4-633922859a8e"), start_time=datetime(year=2022, month=11, day=21, hour=1, minute=57, second=56, tzinfo=offset(offset=timedelta(seconds=-32400.0))), elements=[FRBCUsageForecastElement(duration=Duration.from_timedelta(timedelta(milliseconds=8336)), usage_rate_upper_limit=2600.090517037444, usage_rate_upper_95PPR=5466.368905051084, usage_rate_upper_68PPR=7874.9948212758245, usage_rate_expected=1233.4751600765392, usage_rate_lower_68PPR=1785.90944809586, usage_rate_lower_95PPR=1047.0960233716157, usage_rate_lower_limit=4680.219153555034)])

        # Act
        json_str = frbc_usage_forecast.to_json()

        # Assert
        expected_json = {   'elements': [   {   'duration': 8336,
                        'usage_rate_expected': 1233.4751600765392,
                        'usage_rate_lower_68PPR': 1785.90944809586,
                        'usage_rate_lower_95PPR': 1047.0960233716157,
                        'usage_rate_lower_limit': 4680.219153555034,
                        'usage_rate_upper_68PPR': 7874.9948212758245,
                        'usage_rate_upper_95PPR': 5466.368905051084,
                        'usage_rate_upper_limit': 2600.090517037444}],
    'message_id': '88f742b5-ef8e-4af9-8ae4-633922859a8e',
    'message_type': 'FRBC.UsageForecast',
    'start_time': '2022-11-21T01:57:56-09:00'}
        self.assertEqual(json.loads(json_str), expected_json)
