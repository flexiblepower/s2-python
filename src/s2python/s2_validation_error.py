from dataclasses import dataclass
from typing import Union, Type, Optional

from pydantic import ValidationError


@dataclass
class S2ValidationError(Exception):
    class_: Optional[Type]
    obj: object
    msg: str
    pydantic_validation_error: Union[ValidationError, TypeError, None]
