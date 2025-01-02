import uuid
from typing import List

from s2python.generated.gen_s2 import (
    PEBCPowerConstraints as GenPEBCPowerConstraints,
    PEBCPowerEnvelopeConsequenceType as GenPEBCPowerEnvelopeConsequenceType,
)
from s2python.pebc.pebc_allowed_limit_range import PEBCAllowedLimitRange
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class PEBCPowerConstraints(GenPEBCPowerConstraints, S2Message["PEBCPowerConstraints"]):
    model_config = GenPEBCPowerConstraints.model_config
    model_config["validate_assignment"] = True

    message_id: uuid.UUID = GenPEBCPowerConstraints.model_fields["message_id"]  # type: ignore[assignment]
    id: uuid.UUID = GenPEBCPowerConstraints.model_fields["id"]  # type: ignore[assignment]
    consequence_type: GenPEBCPowerEnvelopeConsequenceType = GenPEBCPowerConstraints.model_fields["consequence_type"]  # type: ignore[assignment]
    allowed_limit_ranges: List[PEBCAllowedLimitRange] = GenPEBCPowerConstraints.model_fields["allowed_limit_ranges"]  # type: ignore[assignment]
    pass 
