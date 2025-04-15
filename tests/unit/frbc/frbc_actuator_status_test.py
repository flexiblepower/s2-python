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
    "active_operation_mode_id": "395dcbc5-5c7f-415e-8727-e48fc53761bc",
    "actuator_id": "1cee425e-861b-417a-8208-bb6d53aafb00",
    "message_id": "07f3d559-63c5-4369-a9e0-deed4195f651",
    "message_type": "FRBC.ActuatorStatus",
    "operation_mode_factor": 6919.960475850124,
    "previous_operation_mode_id": "2ed8f7de-cbaa-4cab-9d25-6792317aa284",
    "transition_timestamp": "2020-01-02T07:56:46Z"
}
        """

        # Act
        frbc_actuator_status = FRBCActuatorStatus.from_json(json_str)

        # Assert
        self.assertEqual(
            frbc_actuator_status.active_operation_mode_id,
            uuid.UUID("395dcbc5-5c7f-415e-8727-e48fc53761bc"),
        )
        self.assertEqual(
            frbc_actuator_status.actuator_id,
            uuid.UUID("1cee425e-861b-417a-8208-bb6d53aafb00"),
        )
        self.assertEqual(
            frbc_actuator_status.message_id,
            uuid.UUID("07f3d559-63c5-4369-a9e0-deed4195f651"),
        )
        self.assertEqual(frbc_actuator_status.message_type, "FRBC.ActuatorStatus")
        self.assertEqual(frbc_actuator_status.operation_mode_factor, 6919.960475850124)
        self.assertEqual(
            frbc_actuator_status.previous_operation_mode_id,
            uuid.UUID("2ed8f7de-cbaa-4cab-9d25-6792317aa284"),
        )
        self.assertEqual(
            frbc_actuator_status.transition_timestamp,
            datetime(
                year=2020,
                month=1,
                day=2,
                hour=7,
                minute=56,
                second=46,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
        )

    def test__to_json__happy_path_full(self):
        # Arrange
        frbc_actuator_status = FRBCActuatorStatus(
            active_operation_mode_id=uuid.UUID("395dcbc5-5c7f-415e-8727-e48fc53761bc"),
            actuator_id=uuid.UUID("1cee425e-861b-417a-8208-bb6d53aafb00"),
            message_id=uuid.UUID("07f3d559-63c5-4369-a9e0-deed4195f651"),
            message_type="FRBC.ActuatorStatus",
            operation_mode_factor=6919.960475850124,
            previous_operation_mode_id=uuid.UUID(
                "2ed8f7de-cbaa-4cab-9d25-6792317aa284"
            ),
            transition_timestamp=datetime(
                year=2020,
                month=1,
                day=2,
                hour=7,
                minute=56,
                second=46,
                tzinfo=offset(offset=timedelta(seconds=0.0)),
            ),
        )

        # Act
        json_str = frbc_actuator_status.to_json()

        # Assert
        expected_json = {
            "active_operation_mode_id": "395dcbc5-5c7f-415e-8727-e48fc53761bc",
            "actuator_id": "1cee425e-861b-417a-8208-bb6d53aafb00",
            "message_id": "07f3d559-63c5-4369-a9e0-deed4195f651",
            "message_type": "FRBC.ActuatorStatus",
            "operation_mode_factor": 6919.960475850124,
            "previous_operation_mode_id": "2ed8f7de-cbaa-4cab-9d25-6792317aa284",
            "transition_timestamp": "2020-01-02T07:56:46Z",
        }
        self.assertEqual(json.loads(json_str), expected_json)
