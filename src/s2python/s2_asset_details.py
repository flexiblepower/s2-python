import logging
import uuid
from dataclasses import dataclass
from typing import Optional, List

from s2python.common import (
    Role,
    ResourceManagerDetails,
    Duration,
    Currency,
)
from s2python.generated.gen_s2 import CommodityQuantity
from s2python.s2_control_type import S2ControlType

logger = logging.getLogger("s2python")


@dataclass
class AssetDetails:  # pylint: disable=too-many-instance-attributes
    resource_id: uuid.UUID

    provides_forecast: bool
    provides_power_measurements: List[CommodityQuantity]

    instruction_processing_delay: Duration
    roles: List[Role]
    currency: Optional[Currency] = None

    name: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    serial_number: Optional[str] = None

    def to_resource_manager_details(
        self, control_types: List[S2ControlType]
    ) -> ResourceManagerDetails:
        return ResourceManagerDetails(
            available_control_types=[
                control_type.get_protocol_control_type()
                for control_type in control_types
            ],
            currency=self.currency,
            firmware_version=self.firmware_version,
            instruction_processing_delay=self.instruction_processing_delay,
            manufacturer=self.manufacturer,
            message_id=uuid.uuid4(),
            model=self.model,
            name=self.name,
            provides_forecast=self.provides_forecast,
            provides_power_measurement_types=self.provides_power_measurements,
            resource_id=self.resource_id,
            roles=self.roles,
            serial_number=self.serial_number,
        )
