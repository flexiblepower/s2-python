import uuid
from datetime import timedelta
import json
from unittest import TestCase

from s2python.common import Transition, Duration
from s2python.s2_validation_error import S2ValidationError


class TransitionTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
        { "id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3",
          "from": "2bdec96b-be3b-4ba9-afa0-c4a0632cced2",
          "to": "2bdec96b-be3b-4ba9-afa0-c4a0632cced1",
          "start_timers": ["2bdec96b-be3b-4ba9-afa0-c4a0632cced4", "2bdec96b-be3b-4ba9-afa0-c4a0632cced5"],
          "blocking_timers": ["2bdec96b-be3b-4ba9-afa0-c4a0632cced4"],
          "transition_costs": 4.3,
          "transition_duration": 1500,
          "abnormal_condition_only": false}
        """

        # Act
        transition: Transition = Transition.from_json(json_str)

        # Assert
        self.assertEqual(
            transition.id, uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3")
        )
        self.assertEqual(
            transition.from_, uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced2")
        )
        self.assertEqual(
            transition.to, uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced1")
        )
        self.assertEqual(
            transition.start_timers,
            [
                uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced4"),
                uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced5"),
            ],
        )
        self.assertEqual(
            transition.blocking_timers,
            [uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced4")],
        )
        self.assertEqual(transition.transition_costs, 4.3)
        assert transition.transition_duration is not None
        self.assertEqual(
            transition.transition_duration.to_timedelta(), timedelta(seconds=1.5)
        )
        self.assertEqual(transition.abnormal_condition_only, False)

    def test__from_json__happy_path_min(self):
        # Arrange
        json_str = """
        { "id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3",
          "from": "2bdec96b-be3b-4ba9-afa0-c4a0632cced2",
          "to": "2bdec96b-be3b-4ba9-afa0-c4a0632cced1",
          "start_timers": [],
          "blocking_timers": [],
          "abnormal_condition_only": true}
        """

        # Act
        transition: Transition = Transition.from_json(json_str)

        # Assert
        self.assertEqual(
            transition.id, uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3")
        )
        self.assertEqual(
            transition.from_, uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced2")
        )
        self.assertEqual(
            transition.to, uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced1")
        )
        self.assertEqual(transition.start_timers, [])
        self.assertEqual(transition.blocking_timers, [])
        self.assertEqual(transition.transition_costs, None)
        self.assertEqual(transition.transition_duration, None)
        self.assertEqual(transition.abnormal_condition_only, True)

    def test__from_json__format_validation_error(self):
        # Arrange
        json_str = """
        { "id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3" }
        """

        # Act / Assert
        with self.assertRaises(S2ValidationError):
            Transition.from_json(json_str)

    def test__from_json__value_validation_error_neg_duration(self):
        # Arrange
        json_str = """
        { "id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3",
          "from": "2bdec96b-be3b-4ba9-afa0-c4a0632cced2",
          "to": "2bdec96b-be3b-4ba9-afa0-c4a0632cced1",
          "start_timers": [],
          "blocking_timers": [],
          "transition_duration": -1500,
          "abnormal_condition_only": true}
        """

        # Act / Assert
        with self.assertRaises(S2ValidationError):
            Transition.from_json(json_str)

    def test__to_json__happy_path(self):
        # Arrange
        # BUG We have to resort to using a dict as we HAVE to pass the 'from' key which is a Python reserved keyword.
        #  We will fix this by moving to pydantic v2 in which aliases have been fixed in which they may be used to
        #  assign values during init. See: https://github.com/flexiblepower/s2-ws-json-python/issues/10
        transition = Transition(
            **{
                "id": uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3"),
                "from": uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced2"),
                "to": uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced1"),
                "start_timers": [],
                "blocking_timers": [],
                "transition_duration": Duration.from_timedelta(
                    timedelta(minutes=1, seconds=1)
                ),
                "abnormal_condition_only": False,
            }
        )

        # Act
        json_str = transition.to_json()

        # Assert
        expected_json = {
            "id": "2bdec96b-be3b-4ba9-afa0-c4a0632cced3",
            "from": "2bdec96b-be3b-4ba9-afa0-c4a0632cced2",
            "to": "2bdec96b-be3b-4ba9-afa0-c4a0632cced1",
            "start_timers": [],
            "blocking_timers": [],
            "transition_duration": 61000,
            "abnormal_condition_only": False,
        }
        self.assertEqual(json.loads(json_str), expected_json)

    def test__to_json__value_validation_error_neg_duration(self):
        # Arrange/ Act / Assert
        with self.assertRaises(S2ValidationError):
            Transition(  # pyright: ignore[reportCallIssue]
                id=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced3"),
                from_=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced2"),
                to=uuid.UUID("2bdec96b-be3b-4ba9-afa0-c4a0632cced1"),
                start_timers=[],
                blocking_timers=[],
                transition_duration=Duration(root=-5000),
                abnormal_condition_only=False,
            )
