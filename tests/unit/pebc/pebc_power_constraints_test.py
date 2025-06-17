from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.pebc import *
from s2python.s2_validation_error import S2ValidationError


class PEBCPowerConstraintsTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """
{
    "message_type": "PEBC.PowerConstraints",
    "message_id": "5165cd7f-04bd-4c78-8fdd-b504cb0013a3",
    "id": "7fe73aa9-1ce0-41e1-9a5f-ea7795687e5e",
    "valid_from": "2025-05-12T12:00:00.000000Z",
    "valid_until": "2025-05-12T13:00:00.000000Z",
    "consequence_type": "VANISH",
    "allowed_limit_ranges": [
        {
            "commodity_quantity": "ELECTRIC.POWER.L1",
            "limit_type": "UPPER_LIMIT",
            "range_boundary": {
                "start_of_range": 0.0,
                "end_of_range": 0.0
            },
            "abnormal_condition_only": false
        },
        {
            "commodity_quantity": "ELECTRIC.POWER.L1",
            "limit_type": "LOWER_LIMIT",
            "range_boundary": {
                "start_of_range": 0.0,
                "end_of_range": -2000.0
            },
            "abnormal_condition_only": false
        }
    ]
}
        """

        # Act
        pebc_power_constraints: PEBCPowerConstraints = PEBCPowerConstraints.from_json(
            json_str
        )

        self.assertEqual(
            pebc_power_constraints.id,
            uuid.UUID("7fe73aa9-1ce0-41e1-9a5f-ea7795687e5e"),
        )
        self.assertEqual(
            pebc_power_constraints.message_id,
            uuid.UUID("5165cd7f-04bd-4c78-8fdd-b504cb0013a3"),
        )
        self.assertEqual(pebc_power_constraints.message_type, "PEBC.PowerConstraints")
        self.assertEqual(
            pebc_power_constraints.consequence_type,
            PEBCPowerEnvelopeConsequenceType.VANISH,
        )

        self.assertEqual(
            pebc_power_constraints.valid_from,
            datetime(
                year=2025,
                month=5,
                day=12,
                hour=12,
                minute=0,
                second=0,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
        )

        self.assertEqual(
            pebc_power_constraints.valid_until,
            datetime(
                year=2025,
                month=5,
                day=12,
                hour=13,
                minute=0,
                second=0,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
        )

        self.assertEqual(len(pebc_power_constraints.allowed_limit_ranges), 2)

    def test__to_json__happy_path(self):
        # Arrange
        pebc_power_constraints = PEBCPowerConstraints(
            message_type="PEBC.PowerConstraints",
            message_id=uuid.UUID("5165cd7f-04bd-4c78-8fdd-b504cb0013a3"),
            id=uuid.UUID("7fe73aa9-1ce0-41e1-9a5f-ea7795687e5e"),
            valid_from=datetime(
                year=2025,
                month=5,
                day=12,
                hour=12,
                minute=0,
                second=0,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
            valid_until=datetime(
                year=2025,
                month=5,
                day=12,
                hour=13,
                minute=0,
                second=0,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
            consequence_type=PEBCPowerEnvelopeConsequenceType.VANISH,
            allowed_limit_ranges=[
                PEBCAllowedLimitRange(
                    commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                    limit_type=PEBCPowerEnvelopeLimitType.UPPER_LIMIT,
                    range_boundary=NumberRange(start_of_range=0.0, end_of_range=0.0),
                    abnormal_condition_only=False,
                ),
                PEBCAllowedLimitRange(
                    commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                    limit_type=PEBCPowerEnvelopeLimitType.LOWER_LIMIT,
                    range_boundary=NumberRange(
                        start_of_range=0.0, end_of_range=-2000.0
                    ),
                    abnormal_condition_only=False,
                ),
            ],
        )

        # Act
        json_str = pebc_power_constraints.to_json()

        # Assert
        expected_json = {
            "message_type": "PEBC.PowerConstraints",
            "message_id": "5165cd7f-04bd-4c78-8fdd-b504cb0013a3",
            "id": "7fe73aa9-1ce0-41e1-9a5f-ea7795687e5e",
            "valid_from": "2025-05-12T12:00:00Z",
            "valid_until": "2025-05-12T13:00:00Z",
            "consequence_type": "VANISH",
            "allowed_limit_ranges": [
                {
                    "commodity_quantity": "ELECTRIC.POWER.L1",
                    "limit_type": "UPPER_LIMIT",
                    "range_boundary": {"start_of_range": 0.0, "end_of_range": 0.0},
                    "abnormal_condition_only": False,
                },
                {
                    "commodity_quantity": "ELECTRIC.POWER.L1",
                    "limit_type": "LOWER_LIMIT",
                    "range_boundary": {"start_of_range": 0.0, "end_of_range": -2000.0},
                    "abnormal_condition_only": False,
                },
            ],
        }
        self.assertEqual(json.loads(json_str), expected_json)

    def test__from_json__missing_upper_limit(self):
        # Arrange
        json_str = """
{
    "message_type": "PEBC.PowerConstraints",
    "message_id": "5165cd7f-04bd-4c78-8fdd-b504cb0013a3",
    "id": "7fe73aa9-1ce0-41e1-9a5f-ea7795687e5e",
    "valid_from": "2025-05-12T12:00:00.000000Z",
    "valid_until": "2025-05-12T13:00:00.000000Z",
    "consequence_type": "VANISH",
    "allowed_limit_ranges": [
        {
            "commodity_quantity": "ELECTRIC.POWER.L1",
            "limit_type": "LOWER_LIMIT",
            "range_boundary": {
                "start_of_range": 0.0,
                "end_of_range": -2000.0
            },
            "abnormal_condition_only": false
        }
    ]
}
        """
        with self.assertRaises(S2ValidationError) as context:
            PEBCPowerConstraints.from_json(json_str)

    def test__from_json__missing_lower_limit(self):
        # Arrange
        json_str = """
{
    "message_type": "PEBC.PowerConstraints",
    "message_id": "5165cd7f-04bd-4c78-8fdd-b504cb0013a3",
    "id": "7fe73aa9-1ce0-41e1-9a5f-ea7795687e5e",
    "valid_from": "2025-05-12T12:00:00.000000Z",
    "valid_until": "2025-05-12T13:00:00.000000Z",
    "consequence_type": "VANISH",
    "allowed_limit_ranges": [
        {
            "commodity_quantity": "ELECTRIC.POWER.L1",
            "limit_type": "UPPER_LIMIT",
            "range_boundary": {
                "start_of_range": 0.0,
                "end_of_range": 0.0
            },
            "abnormal_condition_only": false
        }
    ]
}
        """
        with self.assertRaises(S2ValidationError) as context:
            PEBCPowerConstraints.from_json(json_str)

    def test__from_json__valid_until_before_valid_from(self):
        # Arrange
        json_str = """
{
    "message_type": "PEBC.PowerConstraints",
    "message_id": "5165cd7f-04bd-4c78-8fdd-b504cb0013a3",
    "id": "7fe73aa9-1ce0-41e1-9a5f-ea7795687e5e",
    "valid_from": "2025-05-12T13:00:00.000000Z",
    "valid_until": "2025-05-12T12:00:00.000000Z",
    "consequence_type": "VANISH",
    "allowed_limit_ranges": [
        {
            "commodity_quantity": "ELECTRIC.POWER.L1",
            "limit_type": "UPPER_LIMIT",
            "range_boundary": {
                "start_of_range": 0.0,
                "end_of_range": 0.0
            },
            "abnormal_condition_only": false
        },
        {
            "commodity_quantity": "ELECTRIC.POWER.L1",
            "limit_type": "LOWER_LIMIT",
            "range_boundary": {
                "start_of_range": 0.0,
                "end_of_range": -2000.0
            },
            "abnormal_condition_only": false
        }
    ]
}
        """
        with self.assertRaises(S2ValidationError) as context:
            PEBCPowerConstraints.from_json(json_str)
