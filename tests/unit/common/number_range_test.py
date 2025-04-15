import json
from unittest import TestCase

from s2python.common import NumberRange
from s2python.s2_validation_error import S2ValidationError


class NumberRangeTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = '{"start_of_range": 4.0, "end_of_range": 5.0}'

        # Act
        number_range = NumberRange.from_json(json_str)

        # Assert
        expected_start_of_range = 4.0
        expected_end_of_range = 5.0
        self.assertEqual(number_range.start_of_range, expected_start_of_range)
        self.assertEqual(number_range.end_of_range, expected_end_of_range)

    def test__from_json__happy_path_equals(self):
        # Arrange
        json_str = '{"start_of_range": 4.0, "end_of_range": 5.0}'

        # Act
        number_range = NumberRange.from_json(json_str)

        # Assert
        self.assertEqual(
            number_range, NumberRange(start_of_range=4.0, end_of_range=5.0)
        )

    def test__from_json__format_validation_error(self):
        # Arrange
        json_str = '{"start_of_range": 4.0}'

        # Act / Assert
        with self.assertRaises(S2ValidationError):
            NumberRange.from_json(json_str)

    def test__from_json__end_of_range_smaller_than_start(self):
        # Arrange
        json_str = '{"start_of_range": 6.0, "end_of_range": 5.0}'

        # Act
        number_range = NumberRange.from_json(json_str)

        # Assert
        self.assertEqual(
            number_range, NumberRange(start_of_range=6.0, end_of_range=5.0)
        )

    def test__to_json__happy_path(self):
        # Arrange
        number_range = NumberRange(start_of_range=4.0, end_of_range=5.0)

        # Act
        json_str = number_range.to_json()

        # Assert
        expected_json = {"start_of_range": 4.0, "end_of_range": 5.0}
        self.assertEqual(json.loads(json_str), expected_json)

    def test__to_json__end_of_range_smaller_than_start(self):
        # Arrange
        number_range = NumberRange(start_of_range=6.0, end_of_range=5.0)

        # Act
        json_str = number_range.to_json()

        # Assert
        expected_json = {"start_of_range": 6.0, "end_of_range": 5.0}
        self.assertEqual(json.loads(json_str), expected_json)
