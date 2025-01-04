
from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCInstructionTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "message_type": "FRBC.Instruction",
    "message_id": "e961f92e-32a7-4117-81f3-8868968d2d14",
    "id": "933e2c9c-526a-4934-96de-6eae0ae1f941",
    "actuator_id": "02979ffc-3083-437d-8540-925073dbb465",
    "operation_mode": "90c03b06-728a-4f79-a54b-e01a6bad6f37",
    "operation_mode_factor": 2038.574227328529,
    "execution_time": "2020-07-02T06:03:25+07:00",
    "abnormal_condition": true
}
        """

        # Act
        frbc_instruction = FRBCInstruction.from_json(json_str)

        # Assert
        self.assertEqual(frbc_instruction.message_type, FRBC.Instruction)
        self.assertEqual(frbc_instruction.message_id, uuid.UUID("e961f92e-32a7-4117-81f3-8868968d2d14"))
        self.assertEqual(frbc_instruction.id, uuid.UUID("933e2c9c-526a-4934-96de-6eae0ae1f941"))
        self.assertEqual(frbc_instruction.actuator_id, uuid.UUID("02979ffc-3083-437d-8540-925073dbb465"))
        self.assertEqual(frbc_instruction.operation_mode, uuid.UUID("90c03b06-728a-4f79-a54b-e01a6bad6f37"))
        self.assertEqual(frbc_instruction.operation_mode_factor, 2038.574227328529)
        self.assertEqual(frbc_instruction.execution_time, datetime(year=2020, month=7, day=2, hour=6, minute=3, second=25, tzinfo=offset(offset=timedelta(seconds=25200.0))))
        self.assertEqual(frbc_instruction.abnormal_condition, True)

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_instruction = FRBCInstruction(message_type=FRBC.Instruction, message_id=uuid.UUID("e961f92e-32a7-4117-81f3-8868968d2d14"), id=uuid.UUID("933e2c9c-526a-4934-96de-6eae0ae1f941"), actuator_id=uuid.UUID("02979ffc-3083-437d-8540-925073dbb465"), operation_mode=uuid.UUID("90c03b06-728a-4f79-a54b-e01a6bad6f37"), operation_mode_factor=2038.574227328529, execution_time=datetime(year=2020, month=7, day=2, hour=6, minute=3, second=25, tzinfo=offset(offset=timedelta(seconds=25200.0))), abnormal_condition=True)

        # Act
        json_str = frbc_instruction.to_json()

        # Assert
        expected_json = {   'abnormal_condition': True,
    'actuator_id': '02979ffc-3083-437d-8540-925073dbb465',
    'execution_time': '2020-07-02T06:03:25+07:00',
    'id': '933e2c9c-526a-4934-96de-6eae0ae1f941',
    'message_id': 'e961f92e-32a7-4117-81f3-8868968d2d14',
    'message_type': 'FRBC.Instruction',
    'operation_mode': '90c03b06-728a-4f79-a54b-e01a6bad6f37',
    'operation_mode_factor': 2038.574227328529}
        self.assertEqual(json.loads(json_str), expected_json)
