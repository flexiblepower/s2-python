
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
    "id": "44ea8c08-6aca-4b93-8434-ede68200dc69",
    "diagnostic_label": "some-test-string6411",
    "elements": [
        {
            "fill_level_range": {
                "start_of_range": 13185.562172385307,
                "end_of_range": 28351.769654896747
            },
            "fill_rate": {
                "start_of_range": 25266.999524961477,
                "end_of_range": 34750.38438764264
            },
            "power_ranges": [
                {
                    "start_of_range": 14986.569871211224,
                    "end_of_range": 24935.417325009203,
                    "commodity_quantity": "ELECTRIC.POWER.L1"
                }
            ],
            "running_costs": {
                "start_of_range": 18871.059938463823,
                "end_of_range": 30857.989097156864
            }
        }
    ],
    "abnormal_condition_only": false
}
        """

        # Act
        frbc_operation_mode = FRBCOperationMode.from_json(json_str)

        # Assert
        self.assertEqual(frbc_operation_mode.id, uuid.UUID("44ea8c08-6aca-4b93-8434-ede68200dc69"))
        self.assertEqual(frbc_operation_mode.diagnostic_label, "some-test-string6411")
        self.assertEqual(frbc_operation_mode.elements, [FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=13185.562172385307, end_of_range=28351.769654896747), fill_rate=NumberRange(start_of_range=25266.999524961477, end_of_range=34750.38438764264), power_ranges=[PowerRange(start_of_range=14986.569871211224, end_of_range=24935.417325009203, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=18871.059938463823, end_of_range=30857.989097156864))])
        self.assertEqual(frbc_operation_mode.abnormal_condition_only, False)

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_operation_mode = FRBCOperationMode(id=uuid.UUID("44ea8c08-6aca-4b93-8434-ede68200dc69"), diagnostic_label="some-test-string6411", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=13185.562172385307, end_of_range=28351.769654896747), fill_rate=NumberRange(start_of_range=25266.999524961477, end_of_range=34750.38438764264), power_ranges=[PowerRange(start_of_range=14986.569871211224, end_of_range=24935.417325009203, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=18871.059938463823, end_of_range=30857.989097156864))], abnormal_condition_only=False)

        # Act
        json_str = frbc_operation_mode.to_json()

        # Assert
        expected_json = {   'abnormal_condition_only': False,
    'diagnostic_label': 'some-test-string6411',
    'elements': [   {   'fill_level_range': {   'end_of_range': 28351.769654896747,
                                                'start_of_range': 13185.562172385307},
                        'fill_rate': {   'end_of_range': 34750.38438764264,
                                         'start_of_range': 25266.999524961477},
                        'power_ranges': [   {   'commodity_quantity': 'ELECTRIC.POWER.L1',
                                                'end_of_range': 24935.417325009203,
                                                'start_of_range': 14986.569871211224}],
                        'running_costs': {   'end_of_range': 30857.989097156864,
                                             'start_of_range': 18871.059938463823}}],
    'id': '44ea8c08-6aca-4b93-8434-ede68200dc69'}
        self.assertEqual(json.loads(json_str), expected_json)
