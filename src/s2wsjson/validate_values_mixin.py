from typing import TypeVar, Generic, Protocol, Type, Tuple, Optional

from pydantic import BaseModel, StrBytes, Protocol as PydanticProtocol, ValidationError
import pydantic.main

from s2wsjson.s2_validation_error import S2ValidationError

# Necessary to overwrite validate_model of pydantic to convert ValidationError -> S2ValidationError
pydantic.main.orig_validate_model = pydantic.main.validate_model


def convert_validation_error_to_s2_validation_error(model: Type[BaseModel],
                                                    input_data: 'pydantic.DictStrAny',
                                                    cls: 'pydantic.ModelOrDc' = None) -> Tuple['pydantic.DictStrAny',
                                                                                               'pydantic.SetStr',
                                                                                               Optional[S2ValidationError]]:
    try:
        values, fields_set, validation_error = pydantic.main.orig_validate_model(model, input_data, cls)

        if validation_error:
            validation_error = S2ValidationError(model, 'pydantic had a format validation error', validation_error)

        return values, fields_set, validation_error
    except (ValidationError, TypeError) as e:
        raise S2ValidationError(model, 'pydantic had a format validation error', e)


pydantic.main.validate_model = convert_validation_error_to_s2_validation_error
pydantic.main.BaseModel.__orig_setattr__ = pydantic.main.BaseModel.__setattr__


def wrap__setattr__(self: BaseModel, key, value):
    try:
        self.__orig_setattr__(key, value)
    except (ValidationError, TypeError) as e:
        raise S2ValidationError(self, 'Pydantic raised a format validation error.', pydantic_validation_error=e)


pydantic.main.BaseModel.__setattr__ = wrap__setattr__

B = TypeVar('B', bound=BaseModel, covariant=True)


class SupportsValidation(Protocol[B]):
    # ValidateValuesMixin methods
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


class ValidateValuesMixin(Generic[C]):
    def to_json(self: C) -> str:
        try:
            return self.json()
        except (ValidationError, TypeError) as e:
            raise S2ValidationError(self, 'Pydantic raised a format validation error.', pydantic_validation_error=e)

    def to_dict(self: C) -> dict:
        return self.dict()

    @classmethod
    def from_json(cls: Type[C], json_str: str) -> C:
        gen_model: C = cls.parse_raw(json_str)
        return gen_model
