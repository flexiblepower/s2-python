from dataclasses import dataclass
from typing import Type, Optional


@dataclass
class S2ValidationError(Exception):
    class_: Optional[Type]
    obj: object
    msg: str
