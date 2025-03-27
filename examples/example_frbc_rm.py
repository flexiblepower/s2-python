import argparse
from functools import partial
import logging
import sys
import uuid
import signal
import datetime
from typing import Callable

from s2python.common import (
    EnergyManagementRole,
    Duration,
    Role,
    RoleType,
    Commodity,
    Currency,
    NumberRange,
    PowerRange,
    CommodityQuantity,
)
from s2python.frbc import (
    FRBCInstruction,
    FRBCSystemDescription,
    FRBCActuatorDescription,
    FRBCStorageDescription,
    FRBCOperationMode,
    FRBCOperationModeElement,
    FRBCFillLevelTargetProfile,
    FRBCFillLevelTargetProfileElement,
    FRBCStorageStatus,
    FRBCActuatorStatus,
)
from s2python.s2_connection import S2Connection, AssetDetails
from s2python.s2_control_type import FRBCControlType, NoControlControlType
from s2python.message import S2Message

logger = logging.getLogger("s2python")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


class MyFRBCControlType(FRBCControlType):
    def handle_instruction(
        self, conn: S2Connection, msg: S2Message, send_okay: Callable[[], None]
    ) -> None:
        if not isinstance(msg, FRBCInstruction):
            raise RuntimeError(
                f"Expected an FRBCInstruction but received a message of type {type(msg)}."
            )
        print(f"I have received the message {msg} from {conn}")

    def activate(self, conn: S2Connection) -> None:
        print("The control type FRBC is now activated.")

        print("Time to send a FRBC SystemDescription")
        actuator_id = uuid.uuid4()
        operation_mode_id = uuid.uuid4()
        conn.send_msg_and_await_reception_status_sync(
            FRBCSystemDescription(
                message_id=uuid.uuid4(),
                valid_from=datetime.datetime.now(tz=datetime.timezone.utc),
                actuators=[
                    FRBCActuatorDescription(
                        id=actuator_id,
                        operation_modes=[
                            FRBCOperationMode(
                                id=operation_mode_id,
                                elements=[
                                    FRBCOperationModeElement(
                                        fill_level_range=NumberRange(
                                            start_of_range=0.0, end_of_range=100.0
                                        ),
                                        fill_rate=NumberRange(
                                            start_of_range=-5.0, end_of_range=5.0
                                        ),
                                        power_ranges=[
                                            PowerRange(
                                                start_of_range=-200.0,
                                                end_of_range=200.0,
                                                commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                                            )
                                        ],
                                    )
                                ],
                                diagnostic_label="Load & unload battery",
                                abnormal_condition_only=False,
                            )
                        ],
                        transitions=[],
                        timers=[],
                        supported_commodities=[Commodity.ELECTRICITY],
                    )
                ],
                storage=FRBCStorageDescription(
                    fill_level_range=NumberRange(start_of_range=0.0, end_of_range=100.0),
                    fill_level_label="%",
                    diagnostic_label="Imaginary battery",
                    provides_fill_level_target_profile=True,
                    provides_leakage_behaviour=False,
                    provides_usage_forecast=False,
                ),
            )
        )
        print("Also send the target profile")

        conn.send_msg_and_await_reception_status_sync(
            FRBCFillLevelTargetProfile(
                message_id=uuid.uuid4(),
                start_time=datetime.datetime.now(tz=datetime.timezone.utc),
                elements=[
                    FRBCFillLevelTargetProfileElement(
                        duration=Duration.from_milliseconds(30_000),
                        fill_level_range=NumberRange(start_of_range=20.0, end_of_range=30.0),
                    ),
                    FRBCFillLevelTargetProfileElement(
                        duration=Duration.from_milliseconds(300_000),
                        fill_level_range=NumberRange(start_of_range=40.0, end_of_range=50.0),
                    ),
                ],
            )
        )

        print("Also send the storage status.")
        conn.send_msg_and_await_reception_status_sync(
            FRBCStorageStatus(message_id=uuid.uuid4(), present_fill_level=10.0)
        )

        print("Also send the actuator status.")
        conn.send_msg_and_await_reception_status_sync(
            FRBCActuatorStatus(
                message_id=uuid.uuid4(),
                actuator_id=actuator_id,
                active_operation_mode_id=operation_mode_id,
                operation_mode_factor=0.5,
            )
        )

    def deactivate(self, conn: S2Connection) -> None:
        print("The control type FRBC is now deactivated.")


class MyNoControlControlType(NoControlControlType):
    def activate(self, conn: S2Connection) -> None:
        print("The control type NoControl is now activated.")

    def deactivate(self, conn: S2Connection) -> None:
        print("The control type NoControl is now deactivated.")


def stop(s2_connection, signal_num, _current_stack_frame):
    print(f"Received signal {signal_num}. Will stop S2 connection.")
    s2_connection.stop()


def start_s2_session(url, client_node_id=str(uuid.uuid4())):
    s2_conn = S2Connection(
        url=url,
        role=EnergyManagementRole.RM,
        control_types=[MyFRBCControlType(), MyNoControlControlType()],
        asset_details=AssetDetails(
            resource_id=client_node_id,
            name="Some asset",
            instruction_processing_delay=Duration.from_milliseconds(20),
            roles=[Role(role=RoleType.ENERGY_CONSUMER, commodity=Commodity.ELECTRICITY)],
            currency=Currency.EUR,
            provides_forecast=False,
            provides_power_measurements=[CommodityQuantity.ELECTRIC_POWER_L1],
        ),
        reconnect=True,
        verify_certificate=False,
    )
    signal.signal(signal.SIGINT, partial(stop, s2_conn))
    signal.signal(signal.SIGTERM, partial(stop, s2_conn))

    s2_conn.start_as_rm()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple S2 reseource manager example.")
    parser.add_argument(
        "endpoint",
        type=str,
        help="WebSocket endpoint uri for the server (CEM) e.g. "
        "ws://localhost:8080/backend/rm/s2python-frbc/cem/dummy_model/ws",
    )
    args = parser.parse_args()

    start_s2_session(args.endpoint)
