import abc
from typing import TypeVar, Generic, Protocol, Type

from pydantic import BaseModel, StrBytes, Protocol as PydanticProtocol


B = TypeVar('B', bound=BaseModel, covariant=True)


class SupportsValidation(Protocol[B]):
    # ValidateValuesMixin methods
    def validate_across_values(self) -> bool: ...
    def to_json(self) -> str: ...
    def to_dict(self) -> dict: ...

    @classmethod
    def from_json(cls, json_str: str) -> B: ...

    # Pydantic methods
    def json(self) -> str: ...
    def dict(self) -> dict: ...

    @classmethod
    def parse_raw(cls,
                  b: StrBytes,
                  *,
                  content_type: str = ...,
                  encoding: str = ...,
                  proto: PydanticProtocol = ...,
                  allow_pickle: bool = ...) -> B: ...


C = TypeVar('C', bound='SupportsValidation')


class ValidateValuesMixin(Generic[C], abc.ABC):
    @abc.abstractmethod
    def validate_across_values(self) -> bool:
        pass

    def to_json(self: C) -> str:
        self.validate_across_values()
        return self.json()

    def to_dict(self: C) -> dict:
        self.validate_across_values()
        return self.dict()

    @classmethod
    def from_json(cls: Type[C], json_str: str) -> C:
        gen_model = cls.parse_raw(json_str)
        gen_model.validate_across_values()
        return gen_model
