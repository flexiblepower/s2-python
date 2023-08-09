from unittest import TestCase

from s2wsjson.common import NumberRange, PowerRange
from s2wsjson.frbc.frbc_operation_mode_element import FRBCOperationModeElement
from s2wsjson.generated.gen_s2 import CommodityQuantity


class FRBCOperationModeElementTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = '''
        { "fill_level_range": {"start_of_range": 4.0, "end_of_range": 5.0},
          "fill_rate": {"start_of_range": 0.13, "end_of_range": 10342.569},
          "power_ranges": [{"start_of_range": 400, "end_of_range": 6000, "commodity_quantity": "HYDROGEN.FLOW_RATE"}],
          "running_costs": {"start_of_range": 4.3, "end_of_range": 4.6}}
        '''

        # Act
        element: FRBCOperationModeElement = FRBCOperationModeElement.from_json(json_str)

        # Assert
        expected_fill_level_range = NumberRange(start_of_range=4.0, end_of_range=5.0)
        expected_fill_rate = NumberRange(start_of_range=0.13, end_of_range=10342.569)
        expected_power_ranges = [PowerRange(start_of_range=400,
                                            end_of_range=6000,
                                            commodity_quantity=CommodityQuantity.HYDROGEN_FLOW_RATE)]
        expected_running_costs = NumberRange(start_of_range=4.3, end_of_range=4.6)
        self.assertEqual(element.fill_level_range, expected_fill_level_range)
        self.assertEqual(element.fill_rate, expected_fill_rate)
        self.assertEqual(element.power_ranges, expected_power_ranges)
        self.assertEqual(element.running_costs, expected_running_costs)

    # def test__from_json__format_validation_error(self):
    #     # Arrange
    #     json_str = '{"start_of_range": 4.0}'
    #
    #     # Act / Assert
    #     with self.assertRaises(S2ValidationError):
    #         NumberRange.from_json(json_str)
    #
    # def test__from_json__value_validation_error(self):
    #     # Arrange
    #     json_str = '{"start_of_range": 6.0, "end_of_range": 5.0}'
    #
    #     # Act / Assert
    #     with self.assertRaises(S2ValidationError):
    #         NumberRange.from_json(json_str)
    #
    # def test__to_json__happy_path(self):
    #     # Arrange
    #     number_range = NumberRange(start_of_range=4.0, end_of_range=5.0)
    #
    #     # Act
    #     json = number_range.to_json()
    #
    #     # Assert
    #     expected_json = '{"start_of_range": 4.0, "end_of_range": 5.0}'
    #     self.assertEqual(json, expected_json)
    #
    # def test__to_json__value_validation_error(self):
    #     # Arrange/ Act / Assert
    #     with self.assertRaises(S2ValidationError):
    #         NumberRange(start_of_range=6.0, end_of_range=5.0)
