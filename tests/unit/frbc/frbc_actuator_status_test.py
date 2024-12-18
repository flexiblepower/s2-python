
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
    "message_id": "5d000419-7f2c-451a-b803-ebcc72b7d0bd",
    "actuator_id": "9752ddc9-b04c-4902-a92c-3f181eafd270",
    "active_operation_mode_id": "8d00a902-e202-4c6a-876a-4182bb83c8ac",
    "operation_mode_factor": 39.51079942572766,
    "previous_operation_mode_id": "767ff15a-e406-4ad3-8d74-0f470f9b0589",
    "transition_timestamp": "2022-12-10T08:41:46+07:00"
}
        """

        # Act
        frbc_actuator_status = FRBCActuatorStatus.from_json(json_str)

        # Assert
        self.assertEqual(frbc_actuator_status.message_type, FRBC.ActuatorStatus)
        self.assertEqual(frbc_actuator_status.message_id, uuid.UUID("5d000419-7f2c-451a-b803-ebcc72b7d0bd"))
        self.assertEqual(frbc_actuator_status.actuator_id, uuid.UUID("9752ddc9-b04c-4902-a92c-3f181eafd270"))
        self.assertEqual(frbc_actuator_status.active_operation_mode_id, uuid.UUID("8d00a902-e202-4c6a-876a-4182bb83c8ac"))
        self.assertEqual(frbc_actuator_status.operation_mode_factor, 39.51079942572766)
        self.assertEqual(frbc_actuator_status.previous_operation_mode_id, uuid.UUID("767ff15a-e406-4ad3-8d74-0f470f9b0589"))
        self.assertEqual(frbc_actuator_status.transition_timestamp, datetime(year=2022, month=12, day=10, hour=8, minute=41, second=46, tzinfo=offset(offset=timedelta(seconds=25200.0))))

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_actuator_status = FRBCActuatorStatus(message_type=FRBC.ActuatorStatus, message_id=uuid.UUID("5d000419-7f2c-451a-b803-ebcc72b7d0bd"), actuator_id=uuid.UUID("9752ddc9-b04c-4902-a92c-3f181eafd270"), active_operation_mode_id=uuid.UUID("8d00a902-e202-4c6a-876a-4182bb83c8ac"), operation_mode_factor=39.51079942572766, previous_operation_mode_id=uuid.UUID("767ff15a-e406-4ad3-8d74-0f470f9b0589"), transition_timestamp=datetime(year=2022, month=12, day=10, hour=8, minute=41, second=46, tzinfo=offset(offset=timedelta(seconds=25200.0))))

        # Act
        json_str = frbc_actuator_status.to_json()

        # Assert
        expected_json = {   'active_operation_mode_id': '8d00a902-e202-4c6a-876a-4182bb83c8ac',
    'actuator_id': '9752ddc9-b04c-4902-a92c-3f181eafd270',
    'message_id': '5d000419-7f2c-451a-b803-ebcc72b7d0bd',
    'message_type': 'FRBC.ActuatorStatus',
    'operation_mode_factor': 39.51079942572766,
    'previous_operation_mode_id': '767ff15a-e406-4ad3-8d74-0f470f9b0589',
    'transition_timestamp': '2022-12-10T08:41:46+07:00'}
        self.assertEqual(json.loads(json_str), expected_json)
