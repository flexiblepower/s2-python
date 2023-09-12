import json
import uuid
from datetime import timedelta
from unittest import TestCase

from s2python.common import (
    ResourceManagerDetails,
    CommodityQuantity,
    ControlType,
    Currency,
    Duration,
    Commodity,
    Role,
    RoleType,
)


class ResourceManagerDetailsTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = """{
            "available_control_types": ["POWER_ENVELOPE_BASED_CONTROL", "NOT_CONTROLABLE", "FILL_RATE_BASED_CONTROL"],
            "currency": "CHE",
            "firmware_version": "5.4.2v",
            "instruction_processing_delay": 342,
            "manufacturer": "Dagobert inc.",
            "message_id": "3bdec96b-be3b-4ba9-afa0-c4a0632cced5",
            "message_type": "ResourceManagerDetails",
            "model": "Safe",
            "name": "Dagobert's safe",
            "provides_forecast": true,
            "provides_power_measurement_types": ["HEAT.THERMAL_POWER", "ELECTRIC.POWER.3_PHASE_SYMMETRIC"],
            "resource_id": "3bdec96b-be3b-4ba9-afa0-c4a0632cced6",
            "roles": [{"commodity": "HEAT", "role": "ENERGY_PRODUCER"}, {"commodity": "ELECTRICITY", "role": "ENERGY_CONSUMER"}],
            "serial_number": "safe_batch6_model432"
        }
        """

        # Act
        resource_manager_details: ResourceManagerDetails = (
            ResourceManagerDetails.from_json(json_str)
        )

        # Assert
        self.assertEqual(
            resource_manager_details.available_control_types,
            [
                ControlType.POWER_ENVELOPE_BASED_CONTROL,
                ControlType.NOT_CONTROLABLE,
                ControlType.FILL_RATE_BASED_CONTROL,
            ],
        )
        self.assertEqual(resource_manager_details.currency, Currency.CHE)
        self.assertEqual(resource_manager_details.firmware_version, "5.4.2v")
        self.assertEqual(
            resource_manager_details.instruction_processing_delay,
            Duration.from_timedelta(timedelta(milliseconds=342)),
        )
        self.assertEqual(resource_manager_details.manufacturer, "Dagobert inc.")
        self.assertEqual(
            resource_manager_details.message_id,
            uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632cced5"),
        )
        self.assertEqual(resource_manager_details.model, "Safe")
        self.assertEqual(resource_manager_details.name, "Dagobert's safe")
        self.assertEqual(resource_manager_details.provides_forecast, True)
        self.assertEqual(
            resource_manager_details.provides_power_measurement_types,
            [
                CommodityQuantity.HEAT_THERMAL_POWER,
                CommodityQuantity.ELECTRIC_POWER_3_PHASE_SYMMETRIC,
            ],
        )
        self.assertEqual(
            resource_manager_details.resource_id,
            uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632cced6"),
        )
        self.assertEqual(
            resource_manager_details.roles,
            [
                Role(commodity=Commodity.HEAT, role=RoleType.ENERGY_PRODUCER),
                Role(commodity=Commodity.ELECTRICITY, role=RoleType.ENERGY_CONSUMER),
            ],
        )
        self.assertEqual(resource_manager_details.serial_number, "safe_batch6_model432")

    def test__to_json__happy_path(self):
        # Arrange
        resource_manager_details = ResourceManagerDetails(
            available_control_types=[
                ControlType.POWER_ENVELOPE_BASED_CONTROL,
                ControlType.NOT_CONTROLABLE,
                ControlType.FILL_RATE_BASED_CONTROL,
            ],
            currency=Currency.CHE,
            firmware_version="5.4.2v",
            instruction_processing_delay=Duration.from_timedelta(
                timedelta(milliseconds=342)
            ),
            manufacturer="Dagobert inc.",
            message_id=uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632cced5"),
            model="Safe",
            name="Dagobert's safe",
            provides_forecast=True,
            provides_power_measurement_types=[
                CommodityQuantity.HEAT_THERMAL_POWER,
                CommodityQuantity.ELECTRIC_POWER_3_PHASE_SYMMETRIC,
            ],
            resource_id=uuid.UUID("3bdec96b-be3b-4ba9-afa0-c4a0632cced6"),
            roles=[
                Role(commodity=Commodity.HEAT, role=RoleType.ENERGY_PRODUCER),
                Role(commodity=Commodity.ELECTRICITY, role=RoleType.ENERGY_CONSUMER),
            ],
            serial_number="safe_batch6_model432",
        )

        # Act
        json_str = resource_manager_details.to_json()

        # Assert
        expected_json = {
            "available_control_types": [
                "POWER_ENVELOPE_BASED_CONTROL",
                "NOT_CONTROLABLE",
                "FILL_RATE_BASED_CONTROL",
            ],
            "currency": "CHE",
            "firmware_version": "5.4.2v",
            "instruction_processing_delay": 342,
            "manufacturer": "Dagobert inc.",
            "message_id": "3bdec96b-be3b-4ba9-afa0-c4a0632cced5",
            "message_type": "ResourceManagerDetails",
            "model": "Safe",
            "name": "Dagobert's safe",
            "provides_forecast": True,
            "provides_power_measurement_types": [
                "HEAT.THERMAL_POWER",
                "ELECTRIC.POWER.3_PHASE_SYMMETRIC",
            ],
            "resource_id": "3bdec96b-be3b-4ba9-afa0-c4a0632cced6",
            "roles": [
                {"commodity": "HEAT", "role": "ENERGY_PRODUCER"},
                {"commodity": "ELECTRICITY", "role": "ENERGY_CONSUMER"},
            ],
            "serial_number": "safe_batch6_model432",
        }
        self.assertEqual(json.loads(json_str), expected_json)
