
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
    "message_id": "185b511f-725d-42c8-a1db-523cda5c45a9",
    "id": "8db97bd0-258e-4a8b-92be-40e10b1c7a2c",
    "actuator_id": "cb06550c-e8a2-418d-8885-24a530dde4c4",
    "operation_mode": "4a687962-da90-4379-9190-5d1d68f9dd18",
    "operation_mode_factor": 4456.156981790672,
    "execution_time": "2020-11-11T07:59:54-11:00",
    "abnormal_condition": true
}
        """

        # Act
        frbc_instruction = FRBCInstruction.from_json(json_str)

        # Assert
        self.assertEqual(frbc_instruction.message_type, FRBC.Instruction)
        self.assertEqual(frbc_instruction.message_id, uuid.UUID("185b511f-725d-42c8-a1db-523cda5c45a9"))
        self.assertEqual(frbc_instruction.id, uuid.UUID("8db97bd0-258e-4a8b-92be-40e10b1c7a2c"))
        self.assertEqual(frbc_instruction.actuator_id, uuid.UUID("cb06550c-e8a2-418d-8885-24a530dde4c4"))
        self.assertEqual(frbc_instruction.operation_mode, uuid.UUID("4a687962-da90-4379-9190-5d1d68f9dd18"))
        self.assertEqual(frbc_instruction.operation_mode_factor, 4456.156981790672)
        self.assertEqual(frbc_instruction.execution_time, datetime(year=2020, month=11, day=11, hour=7, minute=59, second=54, tzinfo=offset(offset=timedelta(seconds=-39600.0))))
        self.assertEqual(frbc_instruction.abnormal_condition, True)

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_instruction = FRBCInstruction(message_type=FRBC.Instruction, message_id=uuid.UUID("185b511f-725d-42c8-a1db-523cda5c45a9"), id=uuid.UUID("8db97bd0-258e-4a8b-92be-40e10b1c7a2c"), actuator_id=uuid.UUID("cb06550c-e8a2-418d-8885-24a530dde4c4"), operation_mode=uuid.UUID("4a687962-da90-4379-9190-5d1d68f9dd18"), operation_mode_factor=4456.156981790672, execution_time=datetime(year=2020, month=11, day=11, hour=7, minute=59, second=54, tzinfo=offset(offset=timedelta(seconds=-39600.0))), abnormal_condition=True)

        # Act
        json_str = frbc_instruction.to_json()

        # Assert
        expected_json = {   'abnormal_condition': True,
    'actuator_id': 'cb06550c-e8a2-418d-8885-24a530dde4c4',
    'execution_time': '2020-11-11T07:59:54-11:00',
    'id': '8db97bd0-258e-4a8b-92be-40e10b1c7a2c',
    'message_id': '185b511f-725d-42c8-a1db-523cda5c45a9',
    'message_type': 'FRBC.Instruction',
    'operation_mode': '4a687962-da90-4379-9190-5d1d68f9dd18',
    'operation_mode_factor': 4456.156981790672}
        self.assertEqual(json.loads(json_str), expected_json)
