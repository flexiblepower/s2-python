import uuid
from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase

from s2python.common import (
    PowerForecast,
    Duration,
    PowerForecastValue,
    PowerForecastElement,
    CommodityQuantity,
)


class PowerForecastTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """
        {"elements": [{"duration": 4000, "power_values": [{"commodity_quantity": "NATURAL_GAS.FLOW_RATE", "value_expected": 500.2}]}],
         "message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced9",
         "message_type": "PowerForecast",
         "start_time": "2023-08-02T12:48:42+01:00"}
        """

        # Act
        power_forecast = PowerForecast.from_json(json_str)

        # Assert
        power_forecast_element = PowerForecastElement(
            power_values=[
                PowerForecastValue(  # pyright: ignore[reportCallIssue]
                    commodity_quantity=CommodityQuantity.NATURAL_GAS_FLOW_RATE,
                    value_expected=500.2,
                )
            ],
            duration=Duration.from_timedelta(timedelta(seconds=4)),
        )
        self.assertEqual(power_forecast.elements, [power_forecast_element])
        self.assertEqual(
            power_forecast.message_id, uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced9")
        )
        self.assertEqual(
            power_forecast.start_time,
            datetime(2023, 8, 2, 12, 48, 42, tzinfo=offset(timedelta(hours=1))),
        )

    def test__to_json__happy_path(self):
        # Arrange
        power_forecast_element = PowerForecastElement(
            power_values=[
                PowerForecastValue(  # pyright: ignore[reportCallIssue]
                    commodity_quantity=CommodityQuantity.NATURAL_GAS_FLOW_RATE,
                    value_expected=500.2,
                )
            ],
            duration=Duration.from_timedelta(timedelta(seconds=4)),
        )
        power_forecast = PowerForecast(
            elements=[power_forecast_element],
            message_id=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced9"),
            start_time=datetime(2023, 8, 2, 12, 48, 42, tzinfo=offset(timedelta(hours=2))),
        )

        # Act
        json_str = power_forecast.to_json()

        # Assert
        expected_json = {
            "elements": [
                {
                    "duration": 4000,
                    "power_values": [
                        {
                            "commodity_quantity": "NATURAL_GAS.FLOW_RATE",
                            "value_expected": 500.2,
                        }
                    ],
                }
            ],
            "message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced9",
            "message_type": "PowerForecast",
            "start_time": "2023-08-02T12:48:42+02:00",
        }
        self.assertEqual(json.loads(json_str), expected_json)
