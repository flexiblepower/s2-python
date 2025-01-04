from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import NumberRange, PowerRange
from s2python.frbc.frbc_operation_mode_element import FRBCOperationModeElement
from s2python.generated.gen_s2 import CommodityQuantity


class FRBCOperationModeElementTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "fill_level_range": {
        "end_of_range": 51798.05122344172,
        "start_of_range": 12901.48976850875
    },
    "fill_rate": {
        "end_of_range": 35734.54630113551,
        "start_of_range": 10740.443924585083
    },
    "power_ranges": [
        {
            "commodity_quantity": "ELECTRIC.POWER.L1",
            "end_of_range": 69093.48993128976,
            "start_of_range": 34859.59303603876
        }
    ],
    "running_costs": {
        "end_of_range": 47869.03540464825,
        "start_of_range": 19009.60894672492
    }
}
        """

        # Act
        frbc_operation_mode_element = FRBCOperationModeElement.from_json(json_str)

        # Assert
        self.assertEqual(
            frbc_operation_mode_element.fill_level_range,
            NumberRange(
                end_of_range=51798.05122344172, start_of_range=12901.48976850875
            ),
        )
        self.assertEqual(
            frbc_operation_mode_element.fill_rate,
            NumberRange(
                end_of_range=35734.54630113551, start_of_range=10740.443924585083
            ),
        )
        self.assertEqual(
            frbc_operation_mode_element.power_ranges,
            [
                PowerRange(
                    commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                    end_of_range=69093.48993128976,
                    start_of_range=34859.59303603876,
                )
            ],
        )
        self.assertEqual(
            frbc_operation_mode_element.running_costs,
            NumberRange(
                end_of_range=47869.03540464825, start_of_range=19009.60894672492
            ),
        )

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_operation_mode_element = FRBCOperationModeElement(
            fill_level_range=NumberRange(
                end_of_range=51798.05122344172, start_of_range=12901.48976850875
            ),
            fill_rate=NumberRange(
                end_of_range=35734.54630113551, start_of_range=10740.443924585083
            ),
            power_ranges=[
                PowerRange(
                    commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                    end_of_range=69093.48993128976,
                    start_of_range=34859.59303603876,
                )
            ],
            running_costs=NumberRange(
                end_of_range=47869.03540464825, start_of_range=19009.60894672492
            ),
        )

        # Act
        json_str = frbc_operation_mode_element.to_json()

        # Assert
        expected_json = {
            "fill_level_range": {
                "end_of_range": 51798.05122344172,
                "start_of_range": 12901.48976850875,
            },
            "fill_rate": {
                "end_of_range": 35734.54630113551,
                "start_of_range": 10740.443924585083,
            },
            "power_ranges": [
                {
                    "commodity_quantity": "ELECTRIC.POWER.L1",
                    "end_of_range": 69093.48993128976,
                    "start_of_range": 34859.59303603876,
                }
            ],
            "running_costs": {
                "end_of_range": 47869.03540464825,
                "start_of_range": 19009.60894672492,
            },
        }
        self.assertEqual(json.loads(json_str), expected_json)
