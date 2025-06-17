from datetime import datetime, timezone as offset, timedelta
import json
import uuid
from unittest import TestCase

from s2python.s2_validation_error import S2ValidationError

from s2python.common import PowerMeasurement, PowerValue, CommodityQuantity


class PowerMeasurementTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """
        {"values": [{"commodity_quantity": "OIL.FLOW_RATE", "value": 42.42}],
         "message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced8",
         "message_type": "PowerMeasurement",
         "measurement_timestamp": "2023-08-03T12:48:42+01:00"}
        """

        # Act
        power_measurement: PowerMeasurement = PowerMeasurement.from_json(json_str)

        # Assert
        self.assertEqual(
            power_measurement.message_id,
            uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced8"),
        )
        self.assertEqual(
            power_measurement.measurement_timestamp,
            datetime(2023, 8, 3, 12, 48, 42, tzinfo=offset(timedelta(hours=1))),
        )
        self.assertEqual(
            power_measurement.values,
            [
                PowerValue(
                    commodity_quantity=CommodityQuantity.OIL_FLOW_RATE, value=42.42
                )
            ],
        )

    def test__to_json__happy_path(self):
        # Arrange
        power_measurement = PowerMeasurement(
            values=[
                PowerValue(
                    commodity_quantity=CommodityQuantity.OIL_FLOW_RATE, value=42.42
                )
            ],
            message_id=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced8"),
            measurement_timestamp=datetime(
                2023, 8, 3, 12, 48, 42, tzinfo=offset(timedelta(hours=1))
            ),
        )

        # Act
        json_str = power_measurement.to_json()

        # Assert
        expected_json = {
            "values": [{"commodity_quantity": "OIL.FLOW_RATE", "value": 42.42}],
            "message_id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced8",
            "message_type": "PowerMeasurement",
            "measurement_timestamp": "2023-08-03T12:48:42+01:00",
        }
        self.assertEqual(json.loads(json_str), expected_json)

    def test__init__no_power_measurement_values(self):

        # Arrange / Act / Assert
        with self.assertRaises(S2ValidationError):
            PowerMeasurement(
                values=[],
                message_id=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced8"),
                measurement_timestamp=datetime(
                    2023, 8, 3, 12, 48, 42, tzinfo=offset(timedelta(hours=1))
                ),
            )

    def test__init__multiple_power_measurement_values_for_commodity_quantity(self):

        # Arrange / Act / Assert
        with self.assertRaises(S2ValidationError):
            PowerMeasurement(
                values=[
                    PowerValue(
                        commodity_quantity=CommodityQuantity.OIL_FLOW_RATE, value=42.42
                    ),
                    PowerValue(
                        commodity_quantity=CommodityQuantity.OIL_FLOW_RATE, value=42.42
                    ),
                ],
                message_id=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced8"),
                measurement_timestamp=datetime(
                    2023, 8, 3, 12, 48, 42, tzinfo=offset(timedelta(hours=1))
                ),
            )
