from typing import List
import uuid

from s2python.common.duration import Duration
from s2python.common.role import Role
from s2python.generated.gen_s2 import (
    ResourceManagerDetails as GenResourceManagerDetails,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class ResourceManagerDetails(GenResourceManagerDetails, S2Message["ResourceManagerDetails"]):
    model_config = GenResourceManagerDetails.model_config
    model_config["validate_assignment"] = True

    instruction_processing_delay: Duration = GenResourceManagerDetails.model_fields[
        "instruction_processing_delay"
    ]  # type: ignore[assignment]
    message_id: uuid.UUID = GenResourceManagerDetails.model_fields["message_id"]  # type: ignore[assignment]
    resource_id: uuid.UUID = GenResourceManagerDetails.model_fields["resource_id"]  # type: ignore[assignment]
    roles: List[Role] = GenResourceManagerDetails.model_fields["roles"]  # type: ignore[assignment]
