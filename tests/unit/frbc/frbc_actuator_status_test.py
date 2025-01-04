
from datetime import timedelta, datetime, timezone as offset
import json
from unittest import TestCase
import uuid

from s2python.common import *
from s2python.frbc import *


class FRBCActuatorStatusTest(TestCase):
    def test__from_json__happy_path_full(self):
        # Arrange
        json_str = """
{
    "message_type": "FRBC.ActuatorStatus",
    "message_id": "4dbb1dee-cda6-46d8-92f7-98c1f0cd4157",
    "actuator_id": "0b6552ac-7af4-4627-87da-30fef76d22b7",
    "active_operation_mode_id": "b1ff587d-8257-4644-8adf-7e0a7787863e",
    "operation_mode_factor": 674.4963166817159,
    "previous_operation_mode_id": "7b2553e7-ae6c-4ce4-8059-3712e33b0648",
    "transition_timestamp": "2022-11-24T09:56:49+08:00"
}
        """

        # Act
        frbc_actuator_status = FRBCActuatorStatus.from_json(json_str)

        # Assert
        self.assertEqual(frbc_actuator_status.message_type, FRBC.ActuatorStatus)
        self.assertEqual(frbc_actuator_status.message_id, uuid.UUID("4dbb1dee-cda6-46d8-92f7-98c1f0cd4157"))
        self.assertEqual(frbc_actuator_status.actuator_id, uuid.UUID("0b6552ac-7af4-4627-87da-30fef76d22b7"))
        self.assertEqual(frbc_actuator_status.active_operation_mode_id, uuid.UUID("b1ff587d-8257-4644-8adf-7e0a7787863e"))
        self.assertEqual(frbc_actuator_status.operation_mode_factor, 674.4963166817159)
        self.assertEqual(frbc_actuator_status.previous_operation_mode_id, uuid.UUID("7b2553e7-ae6c-4ce4-8059-3712e33b0648"))
        self.assertEqual(frbc_actuator_status.transition_timestamp, datetime(year=2022, month=11, day=24, hour=9, minute=56, second=49, tzinfo=offset(offset=timedelta(seconds=28800.0))))

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_actuator_status = FRBCActuatorStatus(message_type=FRBC.ActuatorStatus, message_id=uuid.UUID("4dbb1dee-cda6-46d8-92f7-98c1f0cd4157"), actuator_id=uuid.UUID("0b6552ac-7af4-4627-87da-30fef76d22b7"), active_operation_mode_id=uuid.UUID("b1ff587d-8257-4644-8adf-7e0a7787863e"), operation_mode_factor=674.4963166817159, previous_operation_mode_id=uuid.UUID("7b2553e7-ae6c-4ce4-8059-3712e33b0648"), transition_timestamp=datetime(year=2022, month=11, day=24, hour=9, minute=56, second=49, tzinfo=offset(offset=timedelta(seconds=28800.0))))

        # Act
        json_str = frbc_actuator_status.to_json()

        # Assert
        expected_json = {   'active_operation_mode_id': 'b1ff587d-8257-4644-8adf-7e0a7787863e',
    'actuator_id': '0b6552ac-7af4-4627-87da-30fef76d22b7',
    'message_id': '4dbb1dee-cda6-46d8-92f7-98c1f0cd4157',
    'message_type': 'FRBC.ActuatorStatus',
    'operation_mode_factor': 674.4963166817159,
    'previous_operation_mode_id': '7b2553e7-ae6c-4ce4-8059-3712e33b0648',
    'transition_timestamp': '2022-11-24T09:56:49+08:00'}
        self.assertEqual(json.loads(json_str), expected_json)
