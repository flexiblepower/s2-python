from dataclasses import dataclass
from typing import Union, Type, Optional

from pydantic import ValidationError
from pydantic.v1.error_wrappers import ValidationError as ValidationErrorV1


@dataclass
class S2ValidationError(Exception):
    class_: Optional[Type]
    obj: object
    msg: str
    pydantic_validation_error: Union[ValidationErrorV1, ValidationError, TypeError, None]
