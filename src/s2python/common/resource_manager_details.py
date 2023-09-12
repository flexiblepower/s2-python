from typing import List
import uuid

from s2python.common import Duration, Role
from s2python.generated.gen_s2 import (
    ResourceManagerDetails as GenResourceManagerDetails,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    ValidateValuesMixin,
)


@catch_and_convert_exceptions
class ResourceManagerDetails(
    GenResourceManagerDetails, ValidateValuesMixin["ResourceManagerDetails"]
):
    class Config(GenResourceManagerDetails.Config):
        validate_assignment = True

    instruction_processing_delay: Duration = GenResourceManagerDetails.__fields__[
        "instruction_processing_delay"
    ].field_info  # type: ignore[assignment]
    message_id: uuid.UUID = GenResourceManagerDetails.__fields__["message_id"].field_info  # type: ignore[assignment]
    resource_id: uuid.UUID = GenResourceManagerDetails.__fields__["resource_id"].field_info  # type: ignore[assignment]
    roles: List[Role] = GenResourceManagerDetails.__fields__["roles"].field_info  # type: ignore[assignment]
