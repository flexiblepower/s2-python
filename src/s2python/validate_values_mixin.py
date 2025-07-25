from typing import (
    TypeVar,
    Type,
    Callable,
    Any,
    Union,
    AbstractSet,
    Mapping,
    List,
    Dict,
)

from typing_extensions import Self

from pydantic import (  # pylint: disable=no-name-in-module
    BaseModel,
    ValidationError,
)

from s2python.s2_validation_error import S2ValidationError


IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]


class S2MessageComponent(BaseModel):
    def __setattr__(self, name: str, value: Any) -> None:
        try:
            super().__setattr__(name, value)
        except (ValidationError, TypeError) as e:
            raise S2ValidationError(
                type(self), self, "Pydantic raised a validation error.",
            ) from e

    def to_json(self) -> str:
        try:
            return self.model_dump_json(by_alias=True, exclude_none=True)
        except (ValidationError, TypeError) as e:
            raise S2ValidationError(
                type(self), self, "Pydantic raised a validation error.",
            ) from e

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        try:
            gen_model = cls.model_validate_json(json_str)
        except (ValidationError, TypeError) as e:
            raise S2ValidationError(
                type(cls), cls, "Pydantic raised a validation error.",
            ) from e
        return gen_model

    @classmethod
    def from_dict(cls, json_dict: Dict[str, Any]) -> Self:
        try:
            gen_model = cls.model_validate(json_dict)
        except (ValidationError, TypeError) as e:
            raise S2ValidationError(
                type(cls), cls, "Pydantic raised a validation error.",
            ) from e
        return gen_model


def convert_to_s2exception(f: Callable) -> Callable:
    def inner(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            if isinstance(args[0], BaseModel):
                class_type = type(args[0])
                args = args[1:]
            else:
                class_type = None

            raise S2ValidationError(class_type, args, str(e)) from e
        except TypeError as e:
            raise S2ValidationError(None, args, str(e)) from e

    inner.__doc__ = f.__doc__
    inner.__annotations__ = f.__annotations__

    return inner


S = TypeVar("S", bound=S2MessageComponent)


def catch_and_convert_exceptions(input_class: Type[S]) -> Type[S]:
    input_class.__init__ = convert_to_s2exception(input_class.__init__)  # type: ignore[method-assign]

    return input_class
