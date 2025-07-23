import json
from datetime import timedelta
from unittest import TestCase

from s2python.s2_validation_error import S2ValidationError

from s2python.common import (
    PowerForecastElement,
    Duration,
    PowerForecastValue,
    CommodityQuantity,
)


class PowerForecastElementTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = (
            '{"duration": 4000, "power_values": [{"commodity_quantity": "NATURAL_GAS.FLOW_RATE", '
            '"value_expected": 500.2}]}'
        )

        # Act
        power_forecast_element = PowerForecastElement.from_json(json_str)

        # Assert
        self.assertEqual(
            power_forecast_element.duration,
            Duration.from_timedelta(timedelta(seconds=4)),
        )
        self.assertEqual(
            power_forecast_element.power_values,
            [
                PowerForecastValue(  # pyright: ignore[reportCallIssue]
                    commodity_quantity=CommodityQuantity.NATURAL_GAS_FLOW_RATE,
                    value_expected=500.2,
                )
            ],
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

        # Act
        json_str = power_forecast_element.to_json()

        # Assert
        expected_json = {
            "duration": 4000,
            "power_values": [
                {"commodity_quantity": "NATURAL_GAS.FLOW_RATE", "value_expected": 500.2}
            ],
        }
        self.assertEqual(json.loads(json_str), expected_json)

    def test__init__multiple_power_forecast_values_for_commodity_quantity(self):

        # Arrange / Act / Assert
        with self.assertRaises(S2ValidationError):
            PowerForecastElement(
                power_values=[
                    PowerForecastValue(  # pyright: ignore[reportCallIssue]
                        commodity_quantity=CommodityQuantity.NATURAL_GAS_FLOW_RATE,
                        value_expected=500.2,
                    ),

                    PowerForecastValue(  # pyright: ignore[reportCallIssue]
                        commodity_quantity=CommodityQuantity.NATURAL_GAS_FLOW_RATE,
                        value_expected=500.2,
                    )
                ],
                duration=Duration.from_timedelta(timedelta(seconds=4)),
            )
