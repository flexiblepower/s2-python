from typing import Optional


from s2python.generated.gen_s2 import FRBCActuatorStatus as GenFRBCActuatorStatus
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2Message,
)


@catch_and_convert_exceptions
class FRBCActuatorStatus(GenFRBCActuatorStatus, S2Message["FRBCActuatorStatus"]):
    class Config(GenFRBCActuatorStatus.Config):
        validate_assignment = True
