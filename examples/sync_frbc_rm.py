import argparse
import asyncio
import logging
import random
import sys
import threading
import uuid
import signal
import datetime
from typing import Optional

from s2python.common import (
    Duration,
    Role,
    RoleType,
    Commodity,
    Currency,
    NumberRange,
    PowerRange,
    CommodityQuantity,
    PowerMeasurement,
    PowerValue,
)
from s2python.connection.types import S2ConnectionEventsAndMessages, SendOkayRunSync
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
from s2python.connection.sync import S2SyncConnection
from s2python.connection.async_ import WebsocketClientMedium
from s2python.connection.sync.control_type.class_based import (
    FRBCControlType,
    NoControlControlType,
    ResourceManagerHandler,
)

logger = logging.getLogger("s2python")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


class SendPowerMeasurementPeriodically:
    _connection: S2SyncConnection
    _period: datetime.timedelta
    _thread: Optional[threading.Thread]
    _stop: threading.Event

    def __init__(self, connection: S2SyncConnection, period: datetime.timedelta):
        self._connection = connection
        self._period = period
        self._thread = None
        self._stop = threading.Event()

    def _send_power_measurement(self):
        while not self._stop.is_set():
            # Grab the value from an API or anywhere else. Using a random value in this example.
            value = random.uniform(10.0, 100.0)
            print(f"Sending a power measurement message with value={value}")
            self._connection.send_msg_and_await_reception_status(
                PowerMeasurement(
                    message_id=uuid.uuid4(),
                    values=[
                        PowerValue(
                            value=value,
                            commodity_quantity=CommodityQuantity.ELECTRIC_POWER_3_PHASE_SYMMETRIC,
                        )
                    ],
                    measurement_timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
                )
            )
            print("Sent a power measurement message.")
            self._stop.wait(self._period.total_seconds())

    def start(self):
        if self._thread is not None:
            raise RuntimeError("Already started")
        print("Start sending power measurements periodically")
        self._thread = threading.Thread(target=self._send_power_measurement)
        self._thread.start()

    def stop(self):
        if self._thread is None:
            raise RuntimeError("Not started yet")
        self._stop.set()
        self._thread.join(5.0)
        print("Stopped sending power measurements periodically")


class MyFRBCControlType(FRBCControlType):
    def handle_instruction(
        self,
        connection: S2SyncConnection,
        msg: S2ConnectionEventsAndMessages,
        send_okay: SendOkayRunSync,
    ) -> None:
        if not isinstance(msg, FRBCInstruction):
            raise RuntimeError(
                f"Expected an FRBCInstruction but received a message of type {type(msg)}."
            )
        print(f"I have received the message {msg} from {connection}")

    def activate(self, connection: S2SyncConnection) -> None:
        print("The control type FRBC is now activated.")

        print("Time to send a FRBC SystemDescription")
        actuator_id = uuid.uuid4()
        operation_mode_id = uuid.uuid4()
        connection.send_msg_and_await_reception_status(
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
                                                commodity_quantity=CommodityQuantity.ELECTRIC_POWER_3_PHASE_SYMMETRIC,
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

        connection.send_msg_and_await_reception_status(
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
        connection.send_msg_and_await_reception_status(
            FRBCStorageStatus(message_id=uuid.uuid4(), present_fill_level=10.0)
        )

        print("Also send the actuator status.")
        connection.send_msg_and_await_reception_status(
            FRBCActuatorStatus(
                message_id=uuid.uuid4(),
                actuator_id=actuator_id,
                active_operation_mode_id=operation_mode_id,
                operation_mode_factor=0.5,
            )
        )

        self._power_measurement_task = SendPowerMeasurementPeriodically(
            connection, datetime.timedelta(seconds=3)
        )
        self._power_measurement_task.start()

    def deactivate(self, connection: S2SyncConnection) -> None:
        print("The control type FRBC is now deactivated.")
        if self._power_measurement_task is not None:
            self._power_measurement_task.stop()
            self._power_measurement_task = None


class MyNoControlControlType(NoControlControlType):
    def activate(self, connection: S2SyncConnection) -> None:
        print("The control type NoControl is now activated.")

    def deactivate(self, connection: S2SyncConnection) -> None:
        print("The control type NoControl is now deactivated.")


def start_s2_session(url, rm_id: uuid.UUID):
    # Configure a resource manager
    rm_handler = ResourceManagerHandler(
        asset_details=AssetDetails(
            resource_id=rm_id,
            name="Some asset",
            instruction_processing_delay=Duration.from_milliseconds(20),
            roles=[Role(role=RoleType.ENERGY_CONSUMER, commodity=Commodity.ELECTRICITY)],
            currency=Currency.EUR,
            provides_forecast=False,
            provides_power_measurements=[CommodityQuantity.ELECTRIC_POWER_3_PHASE_SYMMETRIC],
        ),
        control_types=[MyFRBCControlType(), MyNoControlControlType()],
    )

    # Setup the underlying websocket connection
    ws_medium = WebsocketClientMedium(url=url, verify_certificate=False)

    eventloop = asyncio.get_event_loop()
    print("Before connecting to websocket")
    eventloop.run_until_complete(ws_medium.connect())
    print("After connecting to websocket")

    # Configure the S2 connection on top of the websocket connection
    s2_conn = S2SyncConnection(medium=ws_medium, eventloop=eventloop)
    rm_handler.register_handlers(s2_conn)

    def stop(signal_num, _current_stack_frame):
        print(f"Received signal {signal_num}. Will stop S2 connection.")
        threading.Thread(target=s2_conn.stop).start()

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    print("Starting s2 connection")
    s2_conn.run()
    print("S2 connection stopped")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple S2 reseource manager example.")
    RM_ID = uuid.uuid4()
    parser.add_argument(
        "--endpoint",
        type=str,
        required=False,
        help=f"WebSocket endpoint uri for the server (CEM) e.g. ws://localhost:8003/ws/{RM_ID}",
        default=f"ws://localhost:8003/ws/{RM_ID}",
    )
    args = parser.parse_args()

    start_s2_session(args.endpoint, RM_ID)
