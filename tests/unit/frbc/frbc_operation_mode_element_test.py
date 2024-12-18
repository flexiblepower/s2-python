
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
        "start_of_range": 2839.6809937410153,
        "end_of_range": 23657.59074127252
    },
    "fill_rate": {
        "start_of_range": 31115.515599679075,
        "end_of_range": 34674.7451119136
    },
    "power_ranges": [
        {
            "start_of_range": 28918.644493729425,
            "end_of_range": 62283.65396785374,
            "commodity_quantity": "ELECTRIC.POWER.L1"
        }
    ],
    "running_costs": {
        "start_of_range": 27450.2722984119,
        "end_of_range": 63683.41689038279
    }
}
        """

        # Act
        frbc_operation_mode_element = FRBCOperationModeElement.from_json(json_str)

        # Assert
        self.assertEqual(frbc_operation_mode_element.fill_level_range, NumberRange(start_of_range=2839.6809937410153, end_of_range=23657.59074127252))
        self.assertEqual(frbc_operation_mode_element.fill_rate, NumberRange(start_of_range=31115.515599679075, end_of_range=34674.7451119136))
        self.assertEqual(frbc_operation_mode_element.power_ranges, [PowerRange(start_of_range=28918.644493729425, end_of_range=62283.65396785374, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)])
        self.assertEqual(frbc_operation_mode_element.running_costs, NumberRange(start_of_range=27450.2722984119, end_of_range=63683.41689038279))

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_operation_mode_element = FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=2839.6809937410153, end_of_range=23657.59074127252), fill_rate=NumberRange(start_of_range=31115.515599679075, end_of_range=34674.7451119136), power_ranges=[PowerRange(start_of_range=28918.644493729425, end_of_range=62283.65396785374, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=27450.2722984119, end_of_range=63683.41689038279))

        # Act
        json_str = frbc_operation_mode_element.to_json()

        # Assert
        expected_json = {   'fill_level_range': {   'end_of_range': 23657.59074127252,
                            'start_of_range': 2839.6809937410153},
    'fill_rate': {   'end_of_range': 34674.7451119136,
                     'start_of_range': 31115.515599679075},
    'power_ranges': [   {   'commodity_quantity': 'ELECTRIC.POWER.L1',
                            'end_of_range': 62283.65396785374,
                            'start_of_range': 28918.644493729425}],
    'running_costs': {   'end_of_range': 63683.41689038279,
                         'start_of_range': 27450.2722984119}}
        self.assertEqual(json.loads(json_str), expected_json)
