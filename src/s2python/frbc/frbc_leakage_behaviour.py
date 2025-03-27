from typing import List
import uuid

from s2python.frbc.frbc_leakage_behaviour_element import FRBCLeakageBehaviourElement
from s2python.generated.gen_s2 import FRBCLeakageBehaviour as GenFRBCLeakageBehaviour
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    S2MessageComponent,
)


@catch_and_convert_exceptions
class FRBCLeakageBehaviour(GenFRBCLeakageBehaviour, S2MessageComponent):
    model_config = GenFRBCLeakageBehaviour.model_config
    model_config["validate_assignment"] = True

    elements: List[FRBCLeakageBehaviourElement] = GenFRBCLeakageBehaviour.model_fields[  # type: ignore[reportIncompatibleVariableOverride]
        "elements"
    ]  # type: ignore[assignment]
    message_id: uuid.UUID = GenFRBCLeakageBehaviour.model_fields["message_id"]  # type: ignore[assignment,reportIncompatibleVariableOverride]
