from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *
from s2python.s2_validation_error import S2ValidationError


class FRBCLeakageBehaviourElementTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "fill_level_range": {
        "end_of_range": 40192.498918818455,
        "start_of_range": 29234.82582981918
    },
    "leakage_rate": 1170.4041485129987
}
        """

        # Act
        frbc_leakage_behaviour_element = FRBCLeakageBehaviourElement.from_json(json_str)

        # Assert
        self.assertEqual(
            frbc_leakage_behaviour_element.fill_level_range,
            NumberRange(
                end_of_range=40192.498918818455, start_of_range=29234.82582981918
            ),
        )
        self.assertEqual(
            frbc_leakage_behaviour_element.leakage_rate, 1170.4041485129987
        )

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_leakage_behaviour_element = FRBCLeakageBehaviourElement(
            fill_level_range=NumberRange(
                end_of_range=40192.498918818455, start_of_range=29234.82582981918
            ),
            leakage_rate=1170.4041485129987,
        )

        # Act
        json_str = frbc_leakage_behaviour_element.to_json()

        # Assert
        expected_json = {
            "fill_level_range": {
                "end_of_range": 40192.498918818455,
                "start_of_range": 29234.82582981918,
            },
            "leakage_rate": 1170.4041485129987,
        }
        self.assertEqual(json.loads(json_str), expected_json)

    def test__init__fill_level_range_end_is_smaller_than_start(self):
        # Arrange / Act / Assert
        with self.assertRaises(S2ValidationError):
            FRBCLeakageBehaviourElement(
                fill_level_range=NumberRange(
                    end_of_range=29234.82582981918, start_of_range=40192.498918818455
                ),
                leakage_rate=1170.4041485129987,
            )
