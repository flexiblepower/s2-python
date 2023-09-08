from s2python.common import NumberRange
from s2python.generated.gen_s2 import (
    FRBCLeakageBehaviourElement as GenFRBCLeakageBehaviourElement,
)
from s2python.validate_values_mixin import (
    catch_and_convert_exceptions,
    ValidateValuesMixin,
)


@catch_and_convert_exceptions
class FRBCLeakageBehaviourElement(
    GenFRBCLeakageBehaviourElement, ValidateValuesMixin["FRBCLeakageBehaviourElement"]
):
    class Config(GenFRBCLeakageBehaviourElement.Config):
        validate_assignment = True

    fill_level_range: NumberRange = GenFRBCLeakageBehaviourElement.__fields__[
        "fill_level_range"
    ].field_info  # type: ignore[assignment]
