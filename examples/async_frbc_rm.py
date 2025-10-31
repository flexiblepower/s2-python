import argparse
import asyncio
from functools import partial
import logging
import sys
import uuid
import signal
import datetime
from typing import Callable

from s2python.common import (
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
from s2python.connection import AssetDetails
from s2python.connection.async_ import S2AsyncConnection
from s2python.connection.async_.medium.websocket import WebsocketClientMedium
from s2python.connection.async_.control_type.class_based import FRBCControlType, NoControlControlType, ResourceManagerHandler
from s2python.message import S2Message

logger = logging.getLogger("s2python")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


class MyFRBCControlType(FRBCControlType):
    async def handle_instruction(
        self, connection: S2AsyncConnection, msg: S2Message, send_okay: Callable[[], None]
    ) -> None:
        if not isinstance(msg, FRBCInstruction):
            raise RuntimeError(
                f"Expected an FRBCInstruction but received a message of type {type(msg)}."
            )
        print(f"I have received the message {msg} from {connection}")

    async def activate(self, connection: S2AsyncConnection) -> None:
        print("The control type FRBC is now activated.")

        print("Time to send a FRBC SystemDescription")
        actuator_id = uuid.uuid4()
        operation_mode_id = uuid.uuid4()
        await connection.send_msg_and_await_reception_status(
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

        await connection.send_msg_and_await_reception_status(
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
        await connection.send_msg_and_await_reception_status(
            FRBCStorageStatus(message_id=uuid.uuid4(), present_fill_level=10.0)
        )

        print("Also send the actuator status.")
        await connection.send_msg_and_await_reception_status(
            FRBCActuatorStatus(
                message_id=uuid.uuid4(),
                actuator_id=actuator_id,
                active_operation_mode_id=operation_mode_id,
                operation_mode_factor=0.5,
            )
        )

    async def deactivate(self, connection: S2AsyncConnection) -> None:
        print("The control type FRBC is now deactivated.")


class MyNoControlControlType(NoControlControlType):
    async def activate(self, connection: S2AsyncConnection) -> None:
        print("The control type NoControl is now activated.")

    async def deactivate(self, connection: S2AsyncConnection) -> None:
        print("The control type NoControl is now deactivated.")


def stop(s2_connection, signal_num, _current_stack_frame):
    print(f"Received signal {signal_num}. Will stop S2 connection.")
    s2_connection.stop()


async def start_s2_session(url, client_node_id=uuid.uuid4()):
    # Configure a resource manager
    rm_handler = ResourceManagerHandler(
        asset_details=AssetDetails(
            resource_id=client_node_id,
            name="Some asset",
            instruction_processing_delay=Duration.from_milliseconds(20),
            roles=[Role(role=RoleType.ENERGY_CONSUMER, commodity=Commodity.ELECTRICITY)],
            currency=Currency.EUR,
            provides_forecast=False,
            provides_power_measurements=[CommodityQuantity.ELECTRIC_POWER_L1],
        ),
        control_types=[MyFRBCControlType(), MyNoControlControlType()]
    )

    # Setup the underlying websocket connection
    ws_medium = WebsocketClientMedium(url=url, verify_certificate=False)
    await ws_medium.connect()

    # Configure the S2 connection on top of the websocket connection
    s2_conn = S2AsyncConnection(medium=ws_medium)
    rm_handler.register_handlers(s2_conn)
    await s2_conn.start()

    signal.signal(signal.SIGINT, partial(stop, s2_conn))
    signal.signal(signal.SIGTERM, partial(stop, s2_conn))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple S2 reseource manager example.")
    parser.add_argument(
        "endpoint",
        type=str,
        help="WebSocket endpoint uri for the server (CEM) e.g. "
        "ws://localhost:8080/backend/rm/s2python-frbc/cem/dummy_model/ws",
    )
    args = parser.parse_args()

    asyncio.run(start_s2_session(args.endpoint))
