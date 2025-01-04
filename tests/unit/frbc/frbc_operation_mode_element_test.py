
from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCOperationModeElementTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "fill_level_range": {
        "start_of_range": 17902.57617756065,
        "end_of_range": 23155.498329551232
    },
    "fill_rate": {
        "start_of_range": 24592.14185864383,
        "end_of_range": 64041.99840646259
    },
    "power_ranges": [
        {
            "start_of_range": 32526.45719448619,
            "end_of_range": 71172.61140295293,
            "commodity_quantity": "ELECTRIC.POWER.L1"
        }
    ],
    "running_costs": {
        "start_of_range": 34310.357669763165,
        "end_of_range": 49896.43882374468
    }
}
        """

        # Act
        frbc_operation_mode_element = FRBCOperationModeElement.from_json(json_str)

        # Assert
        self.assertEqual(frbc_operation_mode_element.fill_level_range, NumberRange(start_of_range=17902.57617756065, end_of_range=23155.498329551232))
        self.assertEqual(frbc_operation_mode_element.fill_rate, NumberRange(start_of_range=24592.14185864383, end_of_range=64041.99840646259))
        self.assertEqual(frbc_operation_mode_element.power_ranges, [PowerRange(start_of_range=32526.45719448619, end_of_range=71172.61140295293, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)])
        self.assertEqual(frbc_operation_mode_element.running_costs, NumberRange(start_of_range=34310.357669763165, end_of_range=49896.43882374468))

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_operation_mode_element = FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=17902.57617756065, end_of_range=23155.498329551232), fill_rate=NumberRange(start_of_range=24592.14185864383, end_of_range=64041.99840646259), power_ranges=[PowerRange(start_of_range=32526.45719448619, end_of_range=71172.61140295293, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=34310.357669763165, end_of_range=49896.43882374468))

        # Act
        json_str = frbc_operation_mode_element.to_json()

        # Assert
        expected_json = {   'fill_level_range': {   'end_of_range': 23155.498329551232,
                            'start_of_range': 17902.57617756065},
    'fill_rate': {   'end_of_range': 64041.99840646259,
                     'start_of_range': 24592.14185864383},
    'power_ranges': [   {   'commodity_quantity': 'ELECTRIC.POWER.L1',
                            'end_of_range': 71172.61140295293,
                            'start_of_range': 32526.45719448619}],
    'running_costs': {   'end_of_range': 49896.43882374468,
                         'start_of_range': 34310.357669763165}}
        self.assertEqual(json.loads(json_str), expected_json)
