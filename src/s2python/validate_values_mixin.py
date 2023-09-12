from typing import (
    TypeVar,
    Generic,
    Protocol,
    Type,
    Tuple,
    Optional,
    Callable,
    cast,
    Any,
    Union,
    AbstractSet,
    Mapping,
    List,
    Dict,
)

from pydantic import BaseModel, StrBytes, Protocol as PydanticProtocol, ValidationError

from s2python.s2_validation_error import S2ValidationError

B = TypeVar("B", bound=BaseModel, covariant=True)

IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]


class SupportsValidation(Protocol[B]):
    # ValidateValuesMixin methods
    def to_json(self) -> str:
        ...

    def to_dict(self) -> dict:
        ...

    @classmethod
    def from_json(cls, json_str: str) -> B:
        ...

    # Pydantic methods
    def json(
        self,
        *,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        ...

    def dict(
        self,
        *,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        ...

    @classmethod
    def parse_raw(
        cls,
        b: StrBytes,
        *,
        content_type: str = ...,
        encoding: str = ...,
        proto: PydanticProtocol = ...,
        allow_pickle: bool = ...,
    ) -> B:
        ...


C = TypeVar("C", bound="SupportsValidation")


class ValidateValuesMixin(Generic[C]):
    def to_json(self: C) -> str:
        try:
            return self.json(by_alias=True, exclude_none=True)
        except (ValidationError, TypeError) as e:
            raise S2ValidationError(
                self, "Pydantic raised a format validation error."
            ) from e

    def to_dict(self: C) -> dict:
        return self.dict()

    @classmethod
    def from_json(cls: Type[C], json_str: str) -> C:
        gen_model: C = cls.parse_raw(json_str)
        return gen_model


def convert_to_s2exception(f: Callable) -> Callable:
    def inner(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        try:
            return f(*args, **kwargs)
        except (ValidationError, TypeError) as e:
            raise S2ValidationError(
                args, "Pydantic raised a format validation error."
            ) from e

    inner.__doc__ = f.__doc__
    inner.__annotations__ = f.__annotations__

    return inner


def catch_and_convert_exceptions(
    input_class: Type[SupportsValidation[B]],
) -> Type[SupportsValidation[B]]:
    input_class.__init__ = convert_to_s2exception(input_class.__init__)  # type: ignore[method-assign]
    input_class.__setattr__ = convert_to_s2exception(input_class.__setattr__)  # type: ignore[method-assign]
    input_class.parse_raw = convert_to_s2exception(input_class.parse_raw)  # type: ignore[method-assign]

    return input_class
