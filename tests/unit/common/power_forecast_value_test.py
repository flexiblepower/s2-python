import json
from unittest import TestCase

from s2python.common import PowerForecastValue, CommodityQuantity


class PowerForecastValueTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """{"commodity_quantity": "HEAT.FLOW_RATE",
                       "value_lower_limit": 450.3,
                       "value_lower_95PPR": 470.4,
                       "value_lower_68PPR": 480.3,
                       "value_expected": 500.2,
                       "value_upper_68PPR": 510.3,
                       "value_upper_95PPR": 515.9,
                       "value_upper_limit": 600}"""

        # Act
        power_forecast_value: PowerForecastValue = PowerForecastValue.from_json(
            json_str
        )

        # Assert
        self.assertEqual(
            power_forecast_value.commodity_quantity, CommodityQuantity.HEAT_FLOW_RATE
        )
        self.assertEqual(power_forecast_value.value_lower_limit, 450.3)
        self.assertEqual(power_forecast_value.value_lower_95PPR, 470.4)
        self.assertEqual(power_forecast_value.value_lower_68PPR, 480.3)
        self.assertEqual(power_forecast_value.value_expected, 500.2)
        self.assertEqual(power_forecast_value.value_upper_68PPR, 510.3)
        self.assertEqual(power_forecast_value.value_upper_95PPR, 515.9)
        self.assertEqual(power_forecast_value.value_upper_limit, 600)

    def test__to_json__happy_path(self):
        # Arrange
        power_forecast_value = PowerForecastValue(  # pyright: ignore[reportCallIssue]
            commodity_quantity=CommodityQuantity.HEAT_TEMPERATURE,
            value_lower_limit=450.3,
            value_lower_95PPR=470.4,
            value_lower_68PPR=480.3,
            value_expected=500.2,
            value_upper_68PPR=510.3,
            value_upper_95PPR=515.9,
            value_upper_limit=600,
        )

        # Act
        json_str = power_forecast_value.to_json()

        # Assert
        expected_json = {
            "commodity_quantity": "HEAT.TEMPERATURE",
            "value_lower_limit": 450.3,
            "value_lower_95PPR": 470.4,
            "value_lower_68PPR": 480.3,
            "value_expected": 500.2,
            "value_upper_68PPR": 510.3,
            "value_upper_95PPR": 515.9,
            "value_upper_limit": 600,
        }
        self.assertEqual(json.loads(json_str), expected_json)

    def test__to_json__only_value_expected(self):
        # Arrange
        power_forecast_value = PowerForecastValue(  # pyright: ignore[reportCallIssue]
            commodity_quantity=CommodityQuantity.HEAT_TEMPERATURE, value_expected=500.2
        )

        # Act
        json_str = power_forecast_value.to_json()

        # Assert
        expected_json = {
            "commodity_quantity": "HEAT.TEMPERATURE",
            "value_expected": 500.2,
        }
        self.assertEqual(json.loads(json_str), expected_json)
