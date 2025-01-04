
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
    "id": "689ee211-83c6-4907-9bde-6ddd47996557",
    "diagnostic_label": "some-test-string8118",
    "elements": [
        {
            "fill_level_range": {
                "start_of_range": 29586.80244711599,
                "end_of_range": 40811.76669416521
            },
            "fill_rate": {
                "start_of_range": 36920.12023083362,
                "end_of_range": 67087.76396982145
            },
            "power_ranges": [
                {
                    "start_of_range": 33844.8053625118,
                    "end_of_range": 67624.38313311148,
                    "commodity_quantity": "ELECTRIC.POWER.L1"
                }
            ],
            "running_costs": {
                "start_of_range": 26024.33483461767,
                "end_of_range": 48053.179872036795
            }
        }
    ],
    "abnormal_condition_only": true
}
        """

        # Act
        frbc_operation_mode = FRBCOperationMode.from_json(json_str)

        # Assert
        self.assertEqual(frbc_operation_mode.id, uuid.UUID("689ee211-83c6-4907-9bde-6ddd47996557"))
        self.assertEqual(frbc_operation_mode.diagnostic_label, "some-test-string8118")
        self.assertEqual(frbc_operation_mode.elements, [FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=29586.80244711599, end_of_range=40811.76669416521), fill_rate=NumberRange(start_of_range=36920.12023083362, end_of_range=67087.76396982145), power_ranges=[PowerRange(start_of_range=33844.8053625118, end_of_range=67624.38313311148, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=26024.33483461767, end_of_range=48053.179872036795))])
        self.assertEqual(frbc_operation_mode.abnormal_condition_only, True)

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_operation_mode = FRBCOperationMode(id=uuid.UUID("689ee211-83c6-4907-9bde-6ddd47996557"), diagnostic_label="some-test-string8118", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=29586.80244711599, end_of_range=40811.76669416521), fill_rate=NumberRange(start_of_range=36920.12023083362, end_of_range=67087.76396982145), power_ranges=[PowerRange(start_of_range=33844.8053625118, end_of_range=67624.38313311148, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=26024.33483461767, end_of_range=48053.179872036795))], abnormal_condition_only=True)

        # Act
        json_str = frbc_operation_mode.to_json()

        # Assert
        expected_json = {   'abnormal_condition_only': True,
    'diagnostic_label': 'some-test-string8118',
    'elements': [   {   'fill_level_range': {   'end_of_range': 40811.76669416521,
                                                'start_of_range': 29586.80244711599},
                        'fill_rate': {   'end_of_range': 67087.76396982145,
                                         'start_of_range': 36920.12023083362},
                        'power_ranges': [   {   'commodity_quantity': 'ELECTRIC.POWER.L1',
                                                'end_of_range': 67624.38313311148,
                                                'start_of_range': 33844.8053625118}],
                        'running_costs': {   'end_of_range': 48053.179872036795,
                                             'start_of_range': 26024.33483461767}}],
    'id': '689ee211-83c6-4907-9bde-6ddd47996557'}
        self.assertEqual(json.loads(json_str), expected_json)
