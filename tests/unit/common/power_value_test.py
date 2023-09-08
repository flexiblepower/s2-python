import json
from unittest import TestCase

from s2python.common import PowerValue, CommodityQuantity


class PowerValueTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = '{"commodity_quantity": "OIL.FLOW_RATE", "value": 43.43}'

        # Act
        power_value: PowerValue = PowerValue.from_json(json_str)

        # Assert
        self.assertEqual(
            power_value.commodity_quantity, CommodityQuantity.OIL_FLOW_RATE
        )
        self.assertEqual(power_value.value, 43.43)

    def test__to_json__happy_path(self):
        # Arrange
        power_value = PowerValue(
            commodity_quantity=CommodityQuantity.OIL_FLOW_RATE, value=43.43
        )

        # Act
        json_str = power_value.to_json()

        # Assert
        expected_json = {"commodity_quantity": "OIL.FLOW_RATE", "value": 43.43}
        self.assertEqual(json.loads(json_str), expected_json)
