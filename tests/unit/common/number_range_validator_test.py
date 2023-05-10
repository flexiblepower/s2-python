from unittest import TestCase

from pydantic import ValidationError

from s2wsjson.common.number_range_validator import NumberRangeValidator


class NumberRangeTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = '{"start_of_range": 4.0, "end_of_range": 5.0}'

        # Act
        number_range = NumberRangeValidator.parse_raw(json_str)

        # Assert
        expected_start_of_range = 4.0
        expected_end_of_range = 5.0
        self.assertEqual(number_range.start_of_range, expected_start_of_range)
        self.assertEqual(number_range.end_of_range, expected_end_of_range)

    def test__from_json__format_validation_error(self):
        # Arrange
        json_str = '{"start_of_range": 4.0}'

        # Act / Assert
        with self.assertRaises(ValidationError):
            NumberRangeValidator.parse_raw(json_str)

    def test__from_json__value_validation_error(self):
        # Arrange
        json_str = '{"start_of_range": 6.0, "end_of_range": 5.0}'

        # Act / Assert
        with self.assertRaises(ValidationError):
            NumberRangeValidator.parse_raw(json_str)

    def test__from_json__validator_error(self):
        # Arrange
        json_str = '{"start_of_range": -6.0, "end_of_range": 5.0}'

        # Act / Assert
        with self.assertRaises(ValidationError):
            NumberRangeValidator.parse_raw(json_str)

    def test__to_json__happy_path(self):
        # Arrange
        number_range = NumberRangeValidator(start_of_range=4.0, end_of_range=5.0)

        # Act
        json = number_range.json()

        # Assert
        expected_json = '{"start_of_range": 4.0, "end_of_range": 5.0}'
        self.assertEqual(json, expected_json)

    def test__to_json__value_validation_error(self):
        # Arrange / Act / Assert
        with self.assertRaises(ValidationError):
            NumberRangeValidator(start_of_range=6.0, end_of_range=5.0)
