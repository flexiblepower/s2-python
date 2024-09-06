from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCLeakageBehaviourTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "elements": [
        {
            "fill_level_range": {
                "end_of_range": 31155.931914859895,
                "start_of_range": 5727.722922773178
            },
            "leakage_rate": 1225.9695121338086
        }
    ],
    "message_id": "b3e9604a-1127-4ecc-9f9e-336047fde285",
    "message_type": "FRBC.LeakageBehaviour",
    "valid_from": "2022-05-26T15:02:32Z"
}
        """

        # Act
        frbc_leakage_behaviour = FRBCLeakageBehaviour.from_json(json_str)

        # Assert
        self.assertEqual(
            frbc_leakage_behaviour.elements,
            [
                FRBCLeakageBehaviourElement(
                    fill_level_range=NumberRange(
                        end_of_range=31155.931914859895,
                        start_of_range=5727.722922773178,
                    ),
                    leakage_rate=1225.9695121338086,
                )
            ],
        )
        self.assertEqual(
            frbc_leakage_behaviour.message_id,
            uuid.UUID("b3e9604a-1127-4ecc-9f9e-336047fde285"),
        )
        self.assertEqual(frbc_leakage_behaviour.message_type, "FRBC.LeakageBehaviour")
        self.assertEqual(
            frbc_leakage_behaviour.valid_from,
            datetime(
                year=2022,
                month=5,
                day=26,
                hour=15,
                minute=2,
                second=32,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
        )

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_leakage_behaviour = FRBCLeakageBehaviour(
            elements=[
                FRBCLeakageBehaviourElement(
                    fill_level_range=NumberRange(
                        end_of_range=31155.931914859895,
                        start_of_range=5727.722922773178,
                    ),
                    leakage_rate=1225.9695121338086,
                )
            ],
            message_id=uuid.UUID("b3e9604a-1127-4ecc-9f9e-336047fde285"),
            message_type="FRBC.LeakageBehaviour",
            valid_from=datetime(
                year=2022,
                month=5,
                day=26,
                hour=15,
                minute=2,
                second=32,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
        )

        # Act
        json_str = frbc_leakage_behaviour.to_json()

        # Assert
        expected_json = {
            "elements": [
                {
                    "fill_level_range": {
                        "end_of_range": 31155.931914859895,
                        "start_of_range": 5727.722922773178,
                    },
                    "leakage_rate": 1225.9695121338086,
                }
            ],
            "message_id": "b3e9604a-1127-4ecc-9f9e-336047fde285",
            "message_type": "FRBC.LeakageBehaviour",
            "valid_from": "2022-05-26T15:02:32Z",
        }
        self.assertEqual(json.loads(json_str), expected_json)
