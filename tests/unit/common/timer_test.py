import uuid
from datetime import timedelta
from unittest import TestCase

from s2wsjson.common import Timer
from s2wsjson.s2_validation_error import S2ValidationError


class TimerTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = '{"id": "2bdec96b-be3b-4ba9-afa0-c4a0632ccedf", "duration": 5000, "diagnostic_label": "some_label"}'

        # Act
        timer = Timer.from_json(json_str)

        # Assert
        expected_id = uuid.UUID('2bdec96b-be3b-4ba9-afa0-c4a0632ccedf')
        expected_duration = timedelta(seconds=5)
        expected_diagnostic_label = 'some_label'
        self.assertEqual(timer.id, expected_id)
        self.assertEqual(timer.duration_as_timedelta(), expected_duration)
        self.assertEqual(timer.diagnostic_label, expected_diagnostic_label)

    def test_optional_parameters(self):
        # Arrange / Act
        timer = Timer(
            id=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632ccedf"),
            duration=timedelta(seconds=5),
        )

        # Assert
        expected_id = uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632ccedf")
        expected_duration = timedelta(seconds=5)

        self.assertIsNone(timer.diagnostic_label)
        self.assertEqual(timer.id, expected_id)
        self.assertEqual(timer.duration_as_timedelta(), expected_duration)

    def test__from_json__format_validation_error(self):
        # Arrange
        json_str = '{"id": "2bdec96b-be3b-4ba9-afa0-c4a0632ccedf", "diagnostic_label": "some_label"}'

        # Act / Assert
        with self.assertRaises(S2ValidationError):
            Timer.from_json(json_str)

    def test__to_json__happy_path(self):
        # Arrange
        timer = Timer(id=uuid.UUID('2bdec96b-be3b-4ba9-afa0-c4a0632ccedf'),
                      duration=timedelta(seconds=5),
                      diagnostic_label='some_label')

        # Act
        json = timer.to_json()

        # Assert
        expected_json = '{"id": "2bdec96b-be3b-4ba9-afa0-c4a0632ccedf", "diagnostic_label": "some_label", "duration": 5000}'
        self.assertEqual(json, expected_json)

    def test__assignment__overriden_duration_field(self):
        # Arrange
        timer = Timer(id=uuid.UUID('2bdec96b-be3b-4ba9-afa0-c4a0632ccedf'),
                      duration=timedelta(seconds=5),
                      diagnostic_label='some_label')

        # Act
        timer.set_duration_as_timedelta(timedelta(seconds=4))

        # Assert
        expected_id = uuid.UUID('2bdec96b-be3b-4ba9-afa0-c4a0632ccedf')
        expected_duration = timedelta(seconds=4)
        expected_diagnostic_label = 'some_label'
        self.assertEqual(timer.id, expected_id)
        self.assertEqual(timer.duration_as_timedelta(), expected_duration)
        self.assertEqual(timer.diagnostic_label, expected_diagnostic_label)
