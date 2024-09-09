import uuid
from typing import (
    TypeVar,
    Generic,
    Protocol,
    Type,
    Optional,
    Callable,
    Any,
    Union,
    AbstractSet,
    Mapping,
    List,
    Dict,
    Literal,
)
from typing_extensions import Self

from pydantic import BaseModel, ValidationError  # pylint: disable=no-name-in-module
from pydantic.main import IncEx
from pydantic.v1.error_wrappers import display_errors  # pylint: disable=no-name-in-module

from s2python.s2_validation_error import S2ValidationError

B_co = TypeVar("B_co", bound=BaseModel, covariant=True)

IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]


class SupportsValidation(Protocol[B_co]):
    # ValidateValuesMixin methods
    def to_json(self) -> str: ...

    def to_dict(self) -> Dict: ...

    @classmethod
    def from_json(cls, json_str: str) -> B_co: ...

    @classmethod
    def from_dict(cls, json_dict: Dict) -> B_co: ...

    # Pydantic methods
    @classmethod
    def model_validate_json(
        cls,
        json_data: Union[str, bytes, bytearray],
        *,
        strict: Optional[bool] = None,
        context: Optional[Any] = None,
    ) -> Self: ...

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: Optional[bool] = None,
        from_attributes: Optional[bool] = None,
        context: Optional[Any] = None,
    ) -> Self: ...

    def model_dump(  # pylint: disable=too-many-arguments
        self,
        *,
        mode: Union[Literal["json", "python"], str] = "python",
        include: IncEx = None,
        exclude: IncEx = None,
        context: Optional[Any] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: Union[bool, Literal["none", "warn", "error"]] = True,
        serialize_as_any: bool = False,
    ) -> Dict[str, Any]: ...

    def model_dump_json(  # pylint: disable=too-many-arguments
        self,
        *,
        indent: Optional[int] = None,
        include: IncEx = None,
        exclude: IncEx = None,
        context: Optional[Any] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: Union[bool, Literal["none", "warn", "error"]] = True,
        serialize_as_any: bool = False,
    ) -> str: ...


C = TypeVar("C", bound="SupportsValidation")


class S2Message(Generic[C]):
    def to_json(self: C) -> str:
        try:
            return self.model_dump_json(by_alias=True, exclude_none=True)
        except (ValidationError, TypeError) as e:
            raise S2ValidationError(
                type(self), self, "Pydantic raised a format validation error.", e
            ) from e

    def to_dict(self: C) -> Dict:
        return self.model_dump()

    @classmethod
    def from_json(cls: Type[C], json_str: str) -> C:
        gen_model: C = cls.model_validate_json(json_str)
        return gen_model

    @classmethod
    def from_dict(cls: Type[C], json_dict: dict) -> C:
        gen_model: C = cls.model_validate(json_dict)
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

            raise S2ValidationError(class_type, args, display_errors(e.errors()), e) from e  # type: ignore[arg-type]
        except TypeError as e:
            raise S2ValidationError(None, args, str(e), e) from e

    inner.__doc__ = f.__doc__
    inner.__annotations__ = f.__annotations__

    return inner


def catch_and_convert_exceptions(
    input_class: Type[SupportsValidation[B_co]],
) -> Type[SupportsValidation[B_co]]:
    input_class.__init__ = convert_to_s2exception(input_class.__init__)  # type: ignore[method-assign]
    input_class.__setattr__ = convert_to_s2exception(input_class.__setattr__)  # type: ignore[method-assign]
    input_class.model_validate_json = convert_to_s2exception(  # type: ignore[method-assign]
        input_class.model_validate_json
    )
    input_class.model_validate = convert_to_s2exception(input_class.model_validate)  # type: ignore[method-assign]

    return input_class
