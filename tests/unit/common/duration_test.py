from datetime import timedelta
from unittest import TestCase

from s2wsjson.common import Duration

class DurationTest(TestCase):
    def test__from_timedelta__happy_path(self):
        # Arrange
        duration_timedelta = timedelta(seconds=10)

        # Act
        duration = Duration.from_timedelta(duration_timedelta)

        # Assert
        self.assertEqual(duration.__root__, 10_000)

    def test__to_timedelta__happy_path(self):
        # Arrange
        duration = Duration(__root__=20_000)

        # Act
        duration_timedelta = duration.to_timedelta()

        # Assert
        self.assertEqual(duration_timedelta, timedelta(milliseconds=20_000))
