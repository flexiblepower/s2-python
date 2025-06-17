from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.pebc import *
from s2python.s2_validation_error import S2ValidationError


class PEBCAllowedLimitRangeTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """
{
    "commodity_quantity": "ELECTRIC.POWER.L1",
    "limit_type": "UPPER_LIMIT",
    "range_boundary": {
        "start_of_range": 0.0,
        "end_of_range": 1000.0
    },
    "abnormal_condition_only": false
}
        """

        # Act
        allowed_limit_range = PEBCAllowedLimitRange.from_json(json_str)

        # Assert
        self.assertEqual(
            allowed_limit_range.commodity_quantity,
            CommodityQuantity.ELECTRIC_POWER_L1,
        )
        self.assertEqual(
            allowed_limit_range.limit_type,
            PEBCPowerEnvelopeLimitType.UPPER_LIMIT,
        )
        self.assertEqual(
            allowed_limit_range.range_boundary.start_of_range, 0.0
        )
        self.assertEqual(
            allowed_limit_range.range_boundary.end_of_range, 1000.0
        )
        self.assertEqual(
            allowed_limit_range.abnormal_condition_only, False
        )

    def test__to_json__happy_path(self):
        # Arrange
        allowed_limit_range = PEBCAllowedLimitRange(
            commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
            limit_type=PEBCPowerEnvelopeLimitType.UPPER_LIMIT,
            range_boundary=NumberRange(
                start_of_range=0.0, end_of_range=1000.0
            ),
            abnormal_condition_only=False,
        )

        # Act
        json_str = allowed_limit_range.to_json()

        # Assert
        expected_json = {
            "commodity_quantity": "ELECTRIC.POWER.L1",
            "limit_type": "UPPER_LIMIT",
            "range_boundary": {"start_of_range": 0.0, "end_of_range": 1000.0},
            "abnormal_condition_only": False,
        }
        self.assertEqual(json.loads(json_str), expected_json)

    def test__from_json__invalid_range_boundary(self):
        # Arrange
        json_str = """
{
    "commodity_quantity": "ELECTRIC.POWER.L1",
    "limit_type": "UPPER_LIMIT",
    "range_boundary": {
        "start_of_range": 1000.0,
        "end_of_range": 0.0
    },
    "abnormal_condition_only": false
}
        """

        # Act & Assert
        with self.assertRaises(S2ValidationError) as context:
            PEBCAllowedLimitRange.from_json(json_str)
