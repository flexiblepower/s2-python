import json
from unittest import TestCase

from s2python.common import PowerRange, CommodityQuantity
from s2python.s2_validation_error import S2ValidationError


class PowerRangeTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = '{"start_of_range": 4.0, "end_of_range": 5.0, "commodity_quantity": "ELECTRIC.POWER.L1"}'

        # Act
        power_range: PowerRange = PowerRange.from_json(json_str)

        # Assert
        expected_start_of_range = 4.0
        expected_end_of_range = 5.0
        self.assertEqual(power_range.start_of_range, expected_start_of_range)
        self.assertEqual(power_range.end_of_range, expected_end_of_range)
        self.assertEqual(
            power_range.commodity_quantity, CommodityQuantity.ELECTRIC_POWER_L1
        )

    def test__from_json__format_validation_error(self):
        # Arrange
        json_str = '{"start_of_range": 4.0}'

        # Act / Assert
        with self.assertRaises(S2ValidationError):
            PowerRange.from_json(json_str)

    def test__from_json__value_validation_error(self):
        # Arrange
        json_str = '{"start_of_range": 6.0, "end_of_range": 5.0, "commodity_quantity": "ELECTRIC.POWER.L1"}'

        # Act / Assert
        with self.assertRaises(S2ValidationError):
            PowerRange.from_json(json_str)

    def test__to_json__happy_path(self):
        # Arrange
        number_range = PowerRange(
            start_of_range=4.0,
            end_of_range=5.0,
            commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
        )

        # Act
        json_str = number_range.to_json()

        # Assert
        expected_json = {
            "start_of_range": 4.0,
            "end_of_range": 5.0,
            "commodity_quantity": "ELECTRIC.POWER.L1",
        }
        self.assertEqual(json.loads(json_str), expected_json)

    def test__to_json__value_validation_error(self):
        # Arrange/ Act / Assert
        with self.assertRaises(S2ValidationError):
            PowerRange(
                start_of_range=6.0,
                end_of_range=5.0,
                commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
            )
