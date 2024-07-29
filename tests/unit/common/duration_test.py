from datetime import timedelta
from unittest import TestCase

from s2python.common import Duration


class DurationTest(TestCase):
    def test__from_timedelta__happy_path(self):
        # Arrange
        duration_timedelta = timedelta(seconds=10)

        # Act
        duration = Duration.from_timedelta(duration_timedelta)

        # Assert
        self.assertEqual(duration.root, 10_000)

    def test__to_timedelta__happy_path(self):
        # Arrange
        duration = Duration(root=20_000)

        # Act
        duration_timedelta = duration.to_timedelta()

        # Assert
        self.assertEqual(duration_timedelta, timedelta(milliseconds=20_000))
