from typing import List, Literal

from pydantic import Field

from s2python.frbc.frbc_leakage_behaviour_element import FRBCLeakageBehaviourElement
from s2python.generated.gen_s2 import FRBCLeakageBehaviour as GenFRBCLeakageBehaviour
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class FRBCLeakageBehaviour(GenFRBCLeakageBehaviour, S2Message["FRBCLeakageBehaviour"]):
    class Config(GenFRBCLeakageBehaviour.Config):
        validate_assignment = True

    elements: List[FRBCLeakageBehaviourElement] = GenFRBCLeakageBehaviour.__fields__[
        "elements"
    ].field_info  # type: ignore[assignment]
    message_type: Literal["FRBC.LeakageBehaviour"] = Field(
        default="FRBC.LeakageBehaviour"
    )
