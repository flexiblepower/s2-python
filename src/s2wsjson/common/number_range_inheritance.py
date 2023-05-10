import abc
from dataclasses import dataclass
from typing import Any, TypeVar, Generic

from pydantic import BaseModel, validator

from s2wsjson.s2_validation_error import S2ValidationError
from s2wsjson.generated.gen_s2 import NumberRange as GenNumberRange

C = TypeVar('C', bound=BaseModel)


class ValidateValuesMixin(Generic[C], abc.ABC):
    @abc.abstractmethod
    def validate_values(self) -> bool:
        pass

    def to_json(self: C) -> str:
        self.validate_values()
        return self.json()

    def to_dict(self: C) -> dict:
        self.validate_values()
        return self.dict()

    @classmethod
    def from_json(cls: C, json_str: str) -> C:
        gen_model = cls.parse_raw(json_str)
        gen_model.validate_values()
        return gen_model


@dataclass
class NumberRangeInherit(GenNumberRange, ValidateValuesMixin):
    def __init__(self, **data: Any):
        super().__init__(**data)

    @validator('start_of_range')
    def validate_start_of_range(cls, v):
        if v < 0:
            raise ValueError('start_of_range should be >= 0')
        return v

    def validate_values(self) -> bool:
        if self.start_of_range > self.end_of_range:
            raise S2ValidationError(self, 'start_of_range should not be higher than end_of_range')

        return True
