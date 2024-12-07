from typing import Literal

from pydantic import Field

from s2python.generated.gen_s2 import FRBCInstruction as GenFRBCInstruction
from s2python.validate_values_mixin import S2Message, catch_and_convert_exceptions


@catch_and_convert_exceptions
class FRBCInstruction(GenFRBCInstruction, S2Message["FRBCInstruction"]):
    class Config(GenFRBCInstruction.Config):
        validate_assignment = True

    message_type: Literal["FRBC.Instruction"] = Field(default="FRBC.Instruction")
