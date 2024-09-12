from typing import TypeVar, Generic, Type, Callable, Any, Union, AbstractSet, Mapping, List, Dict

from pydantic import BaseModel, ValidationError  # pylint: disable=no-name-in-module
from pydantic.v1.error_wrappers import display_errors  # pylint: disable=no-name-in-module

from s2python.s2_validation_error import S2ValidationError

B_co = TypeVar("B_co", bound=BaseModel, covariant=True)

IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]


C = TypeVar("C", bound="BaseModel")


class S2Message(BaseModel, Generic[C]):
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


def catch_and_convert_exceptions(input_class: Type[S2Message[B_co]]) -> Type[S2Message[B_co]]:
    input_class.__init__ = convert_to_s2exception(input_class.__init__)  # type: ignore[method-assign]
    input_class.__setattr__ = convert_to_s2exception(input_class.__setattr__)  # type: ignore[method-assign]
    input_class.model_validate_json = convert_to_s2exception(  # type: ignore[method-assign]
        input_class.model_validate_json
    )
    input_class.model_validate = convert_to_s2exception(input_class.model_validate)  # type: ignore[method-assign]

    return input_class
