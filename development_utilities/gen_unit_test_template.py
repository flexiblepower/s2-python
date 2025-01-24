import datetime
import json
import os
from enum import Enum
import inspect
import pprint
import random
from typing import (
    get_type_hints,
    Type,
    get_origin,
    get_args,
    Union,
    TypeVar,
    Callable,
    Sequence,
)
import uuid

import pydantic
from pydantic.types import AwareDatetime

from s2python import frbc
from s2python.common import Duration, PowerRange, NumberRange
from s2python.generated.gen_s2 import CommodityQuantity

I = TypeVar("I")


def split_words_list(list_: Sequence[I], is_sep: Callable[[I], bool]) -> list[list[I]]:
    words = []
    current_word = []
    previous_was_sep = None
    for item in list_:
        current_is_sep = is_sep(item)

        if previous_was_sep is None:
            previous_was_sep = current_is_sep

        if not previous_was_sep and current_is_sep:
            # Split detected
            words.append(current_word)
            current_word = [item]
        else:
            current_word.append(item)

        previous_was_sep = current_is_sep
    words.append(current_word)
    return words


def is_optional(field_type):
    return get_origin(field_type) is Union and type(None) in get_args(field_type)


def get_optional_arg(field_type):
    return next(type_ for type_ in get_args(field_type) if type_ is not type(None))


def is_list(field_type):
    return get_origin(field_type) is list


def get_list_arg(field_type):
    return get_args(field_type)[0]


def is_enum(field_type):
    return inspect.isclass(field_type) and issubclass(field_type, Enum)


def snake_case(camelcased: str) -> str:
    device_type = camelcased[0:4].lower()
    class_name = camelcased[4:]
    words = split_words_list(class_name, lambda c: c.isupper())
    return "_".join([device_type] + ["".join(word).lower() for word in words])


def message_type_from_class_name(class_name: str) -> str:
    return f"{class_name[0:4]}.{class_name[4:]}"


def generate_json_test_data_for_field(field_type: Type):
    if field_type is Duration:
        value = random.randint(0, 39999)
    elif field_type is NumberRange:
        start = random.random()
        offset = random.random()
        value = {
            "start_of_range": start * 39999,
            "end_of_range": (start + offset) * 39999,
        }
    elif field_type is PowerRange:
        start = random.random()
        offset = random.random()
        value = {
            "start_of_range": start * 39999,
            "end_of_range": (start + offset) * 39999,
            "commodity_quantity": generate_json_test_data_for_field(CommodityQuantity),
        }
    elif inspect.isclass(field_type) and issubclass(field_type, pydantic.BaseModel):
        value = generate_json_test_data_for_class(field_type)
    elif is_list(field_type):
        value = [generate_json_test_data_for_field(get_list_arg(field_type))]
    elif is_optional(field_type):
        value = generate_json_test_data_for_field(get_optional_arg(field_type))
    elif is_enum(field_type):
        field_type: Enum
        value = next(value for value in field_type).value
    elif field_type is str:
        value = f"some-test-string{random.randint(0, 9999)}"
    elif field_type is bool:
        value = bool(random.randint(0, 1))
    elif field_type is float:
        value = random.random() * 9000.0
    elif field_type in (AwareDatetime, datetime.datetime):
        # Generate a timezone-aware datetime
        value = datetime.datetime(
            year=random.randint(2020, 2023),
            month=random.randint(1, 12),
            day=random.randint(1, 28),
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59),
            tzinfo=datetime.timezone(datetime.timedelta(hours=random.randint(-12, 14))),
        )
    elif field_type is uuid.UUID:
        value = uuid.uuid4()
    else:
        raise RuntimeError(f"Please implement test data for field type {field_type}")
    return value


def generate_json_test_data_for_class(class_: Type) -> dict:
    result = {}
    for field_name, field_type in get_type_hints(class_).items():
        if field_name == "message_type":
            result[field_name] = message_type_from_class_name(class_.__name__)
        else:
            result[field_name] = generate_json_test_data_for_field(field_type)

    return result


def dump_test_data_as_constructor_field_for(test_data, field_type: Type) -> str:
    if field_type is Duration:
        value = f"Duration.from_timedelta(timedelta(milliseconds={test_data}))"
    elif inspect.isclass(field_type) and issubclass(field_type, pydantic.BaseModel):
        value = dump_test_data_as_constructor_for(test_data, field_type)
    elif is_list(field_type):
        dumped_items = [
            dump_test_data_as_constructor_field_for(
                test_data_item, get_list_arg(field_type)
            )
            for test_data_item in test_data
        ]
        value = f'[{",".join(dumped_items)}]'
    elif is_optional(field_type):
        value = dump_test_data_as_constructor_field_for(
            test_data, get_optional_arg(field_type)
        )
    elif is_enum(field_type):
        field_type: Enum
        value = f'{field_type.__name__}.{test_data.replace(".", "_")}'
    elif field_type is str:
        value = f'"{test_data}"'
    elif field_type is bool:
        value = str(test_data)
    elif field_type is float:
        value = str(test_data)
    elif field_type is AwareDatetime or field_type is datetime.datetime:
        test_data: datetime.datetime
        offset: datetime.timedelta = test_data.tzinfo.utcoffset(None)
        value = (
            f"datetime("
            f"year={test_data.year}, month={test_data.month}, day={test_data.day}, "
            f"hour={test_data.hour}, minute={test_data.minute}, second={test_data.second}, "
            f"tzinfo=offset(offset=timedelta(seconds={offset.total_seconds()})))"
        )
    elif field_type is uuid.UUID:
        value = f'uuid.UUID("{test_data}")'
    elif type(field_type).__name__ == "_LiteralGenericAlias":
        value = field_type.__args__[0]
    else:
        raise RuntimeError(
            f"Please implement dump test data for field type {field_type}"
        )
    return value


def dump_test_data_as_constructor_for(test_data: dict, class_: Type) -> str:
    result = f"{class_.__name__}"

    first = True
    for field_name, field_type in get_type_hints(class_).items():
        value = dump_test_data_as_constructor_field_for(
            test_data[field_name], field_type
        )
        result += f'{"(" if first else ", "}{field_name}={value}'
        first = False

    return result + ")"


def dump_test_data_as_json_field_for(test_data, field_type: Type):
    if field_type is Duration:
        value = test_data
    elif inspect.isclass(field_type) and issubclass(field_type, pydantic.BaseModel):
        value = dump_test_data_as_json_for(test_data, field_type)
    elif is_list(field_type):
        value = [
            dump_test_data_as_json_field_for(item, get_list_arg(field_type))
            for item in test_data
        ]
    elif is_optional(field_type):
        value = dump_test_data_as_json_field_for(
            test_data, get_optional_arg(field_type)
        )
    elif is_enum(field_type):
        field_type: Enum
        value = test_data
    elif field_type is str:
        value = test_data
    elif field_type is bool:
        value = test_data
    elif field_type is float:
        value = test_data
    elif field_type in (AwareDatetime, datetime.datetime):
        test_data: datetime.datetime
        value = test_data.isoformat()
    elif field_type is uuid.UUID:
        value = str(test_data)
    elif type(field_type).__name__ == "_LiteralGenericAlias":
        value = test_data
    else:
        raise RuntimeError(
            f"Please implement dump test data to json for field type {field_type}"
        )

    return value


def dump_test_data_as_json_for(test_data: dict, class_: Type) -> dict:
    result = {}

    for field_name, field_type in get_type_hints(class_).items():
        result[field_name] = dump_test_data_as_json_field_for(
            test_data[field_name], field_type
        )

    return result


for class_name, class_ in inspect.getmembers(frbc):
    if inspect.isclass(class_) and issubclass(class_, pydantic.BaseModel):
        test_data = generate_json_test_data_for_class(class_)

        assert_lines = []
        for field_name, field_type in get_type_hints(class_).items():
            assert_test_data = dump_test_data_as_constructor_field_for(
                test_data[field_name], field_type
            )

            assert_lines.append(
                f"self.assertEqual({snake_case(class_name)}.{field_name}, {assert_test_data})"
            )

        asserts = "\n        ".join(assert_lines)
        template = f"""
from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class {class_name}Test(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = \"\"\"
{json.dumps(dump_test_data_as_json_for(test_data, class_), indent=4)}
        \"\"\"

        # Act
        {snake_case(class_name)} = {class_name}.from_json(json_str)

        # Assert
        {asserts}

    def test__to_json__happy_path_full(self):
        # Arrange
        {snake_case(class_name)} = {dump_test_data_as_constructor_for(test_data, class_)}

        # Act
        json_str = {snake_case(class_name)}.to_json()

        # Assert
        expected_json = {pprint.pformat(dump_test_data_as_json_for(test_data, class_), indent=4)}
        self.assertEqual(json.loads(json_str), expected_json)
"""
        print(template)
        print()
        print()

        # Check if the file already exists
        if not os.path.exists(f"tests/unit/frbc/{snake_case(class_name)}_test.py"):
            with open(
                f"tests/unit/frbc/{snake_case(class_name)}_test.py", "w+"
            ) as unit_test_file:
                unit_test_file.write(template)
                print(f"Created tests/unit/frbc/{snake_case(class_name)}_test.py")
