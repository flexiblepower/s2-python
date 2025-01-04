from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCOperationModeTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "abnormal_condition_only": true,
    "diagnostic_label": "some-test-string7557",
    "elements": [
        {
            "fill_level_range": {
                "end_of_range": 34304.92092046668,
                "start_of_range": 17579.18236077446
            },
            "fill_rate": {
                "end_of_range": 41719.931165871916,
                "start_of_range": 10542.600445486576
            },
            "power_ranges": [
                {
                    "commodity_quantity": "ELECTRIC.POWER.L1",
                    "end_of_range": 44983.5145552435,
                    "start_of_range": 29337.138579372047
                }
            ],
            "running_costs": {
                "end_of_range": 62835.00070350196,
                "start_of_range": 33318.34845926906
            }
        }
    ],
    "id": "b1255236-475c-4dc7-a728-afb620a99ec8"
}
        """

        # Act
        frbc_operation_mode = FRBCOperationMode.from_json(json_str)

        # Assert
        self.assertEqual(frbc_operation_mode.abnormal_condition_only, True)
        self.assertEqual(frbc_operation_mode.diagnostic_label, "some-test-string7557")
        self.assertEqual(
            frbc_operation_mode.elements,
            [
                FRBCOperationModeElement(
                    fill_level_range=NumberRange(
                        end_of_range=34304.92092046668, start_of_range=17579.18236077446
                    ),
                    fill_rate=NumberRange(
                        end_of_range=41719.931165871916,
                        start_of_range=10542.600445486576,
                    ),
                    power_ranges=[
                        PowerRange(
                            commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                            end_of_range=44983.5145552435,
                            start_of_range=29337.138579372047,
                        )
                    ],
                    running_costs=NumberRange(
                        end_of_range=62835.00070350196, start_of_range=33318.34845926906
                    ),
                )
            ],
        )
        self.assertEqual(
            frbc_operation_mode.id, uuid.UUID("b1255236-475c-4dc7-a728-afb620a99ec8")
        )

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_operation_mode = FRBCOperationMode(
            abnormal_condition_only=True,
            diagnostic_label="some-test-string7557",
            elements=[
                FRBCOperationModeElement(
                    fill_level_range=NumberRange(
                        end_of_range=34304.92092046668, start_of_range=17579.18236077446
                    ),
                    fill_rate=NumberRange(
                        end_of_range=41719.931165871916,
                        start_of_range=10542.600445486576,
                    ),
                    power_ranges=[
                        PowerRange(
                            commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                            end_of_range=44983.5145552435,
                            start_of_range=29337.138579372047,
                        )
                    ],
                    running_costs=NumberRange(
                        end_of_range=62835.00070350196, start_of_range=33318.34845926906
                    ),
                )
            ],
            id=uuid.UUID("b1255236-475c-4dc7-a728-afb620a99ec8"),
        )

        # Act
        json_str = frbc_operation_mode.to_json()

        # Assert
        expected_json = {
            "abnormal_condition_only": True,
            "diagnostic_label": "some-test-string7557",
            "elements": [
                {
                    "fill_level_range": {
                        "end_of_range": 34304.92092046668,
                        "start_of_range": 17579.18236077446,
                    },
                    "fill_rate": {
                        "end_of_range": 41719.931165871916,
                        "start_of_range": 10542.600445486576,
                    },
                    "power_ranges": [
                        {
                            "commodity_quantity": "ELECTRIC.POWER.L1",
                            "end_of_range": 44983.5145552435,
                            "start_of_range": 29337.138579372047,
                        }
                    ],
                    "running_costs": {
                        "end_of_range": 62835.00070350196,
                        "start_of_range": 33318.34845926906,
                    },
                }
            ],
            "id": "b1255236-475c-4dc7-a728-afb620a99ec8",
        }
        self.assertEqual(json.loads(json_str), expected_json)
