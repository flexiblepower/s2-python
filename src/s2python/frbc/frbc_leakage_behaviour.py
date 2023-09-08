from typing import List
import uuid

from s2python.frbc import FRBCLeakageBehaviourElement
from s2python.generated.gen_s2 import FRBCLeakageBehaviour as GenFRBCLeakageBehaviour
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    ValidateValuesMixin,
)


@catch_and_convert_exceptions
class FRBCLeakageBehaviour(
    GenFRBCLeakageBehaviour, ValidateValuesMixin["FRBCLeakageBehaviour"]
):
    class Config(GenFRBCLeakageBehaviour.Config):
        validate_assignment = True

    elements: List[FRBCLeakageBehaviourElement] = GenFRBCLeakageBehaviour.__fields__[
        "elements"
    ].field_info  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCLeakageBehaviour.__fields__["message_id"].field_info  # type: ignore[assignment]
