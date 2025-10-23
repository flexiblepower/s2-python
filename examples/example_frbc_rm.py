import argparse
from functools import partial
import logging
import sys
import uuid
import signal
import datetime
import time
import threading
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
    Timer,
    Transition,
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
from s2python.communication.s2_connection import S2Connection, AssetDetails
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

        print("Creating a FRBC device with proper transitions and timers")
        
        # Create charge and off operation modes like in example_schedule_frbc.py
        actuator_id = uuid.uuid4()
        charge_operation_mode_id = uuid.uuid4()
        off_operation_mode_id = uuid.uuid4()
        
        # Create timers for transitions (needed for proper FRBC operation)
        on_to_off_timer_id = uuid.uuid4()
        off_to_on_timer_id = uuid.uuid4()
        
        # Create transitions between modes
        transition_on_to_off_id = uuid.uuid4()
        transition_off_to_on_id = uuid.uuid4()
        
        print("Time to send a FRBC SystemDescription")
        conn.send_msg_and_await_reception_status_sync(
            FRBCSystemDescription(
                message_id=uuid.uuid4(),
                valid_from=datetime.datetime.now(tz=datetime.timezone.utc),
                actuators=[
                    FRBCActuatorDescription(
                        id=actuator_id,
                        operation_modes=[
                            # Charging mode - similar to recharge system description from example
                            FRBCOperationMode(
                                id=charge_operation_mode_id,
                                elements=[
                                    FRBCOperationModeElement(
                                        fill_level_range=NumberRange(
                                            start_of_range=0.0, end_of_range=100.0
                                        ),
                                        fill_rate=NumberRange(
                                            start_of_range=0.0, end_of_range=0.01099537114  # Charge power from example
                                        ),
                                        power_ranges=[
                                            PowerRange(
                                                start_of_range=0.0,
                                                end_of_range=57000.0,  # 57kW from example
                                                commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                                            )
                                        ],
                                    )
                                ],
                                diagnostic_label="charge.on",
                                abnormal_condition_only=False,
                            ),
                            # Off mode - similar to driving/off system description from example
                            FRBCOperationMode(
                                id=off_operation_mode_id,
                                elements=[
                                    FRBCOperationModeElement(
                                        fill_level_range=NumberRange(
                                            start_of_range=0.0, end_of_range=100.0
                                        ),
                                        fill_rate=NumberRange(
                                            start_of_range=0.0, end_of_range=0.0
                                        ),
                                        power_ranges=[
                                            PowerRange(
                                                start_of_range=0.0,
                                                end_of_range=0.0,
                                                commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
                                            )
                                        ],
                                    )
                                ],
                                diagnostic_label="charge.off",
                                abnormal_condition_only=False,
                            )
                        ],
                        transitions=[
                            # Transition from charging to off
                            Transition(
                                id=transition_on_to_off_id,
                                **{"from": charge_operation_mode_id},
                                to=off_operation_mode_id,
                                start_timers=[off_to_on_timer_id],
                                blocking_timers=[on_to_off_timer_id],
                                transition_duration=None,
                                abnormal_condition_only=False
                            ),
                            # Transition from off to charging  
                            Transition(
                                id=transition_off_to_on_id,
                                **{"from": off_operation_mode_id},
                                to=charge_operation_mode_id,
                                start_timers=[on_to_off_timer_id],
                                blocking_timers=[off_to_on_timer_id],
                                transition_duration=None,
                                abnormal_condition_only=False
                            )
                        ],
                        timers=[
                            # Timer for on to off transition
                            Timer(
                                id=on_to_off_timer_id,
                                diagnostic_label="charge_on.to.off.timer",
                                duration=Duration.from_milliseconds(30000)  # 30 seconds
                            ),
                            # Timer for off to on transition
                            Timer(
                                id=off_to_on_timer_id,
                                diagnostic_label="charge_off.to.on.timer", 
                                duration=Duration.from_milliseconds(30000)  # 30 seconds
                            )
                        ],
                        supported_commodities=[Commodity.ELECTRICITY],
                    )
                ],
                storage=FRBCStorageDescription(
                    fill_level_range=NumberRange(
                        start_of_range=0.0, end_of_range=100.0
                    ),
                    fill_level_label="SoC %",
                    diagnostic_label="battery",
                    provides_fill_level_target_profile=True,
                    provides_leakage_behaviour=False,
                    provides_usage_forecast=False,
                ),
            )
        )
        
        print("Send fill level target profile - similar to example pattern")
        # Create a target profile similar to the example with charging goals
        conn.send_msg_and_await_reception_status_sync(
            FRBCFillLevelTargetProfile(
                message_id=uuid.uuid4(),
                start_time=datetime.datetime.now(tz=datetime.timezone.utc),
                elements=[
                    # First period: charge to higher level (similar to recharge period from example)
                    FRBCFillLevelTargetProfileElement(
                        duration=Duration.from_milliseconds(1800000),  # 30 minutes
                        fill_level_range=NumberRange(
                            start_of_range=80.0, end_of_range=100.0  # Target high charge
                        ),
                    ),
                    # Second period: maintain level
                    FRBCFillLevelTargetProfileElement(
                        duration=Duration.from_milliseconds(1800000),  # 30 minutes  
                        fill_level_range=NumberRange(
                            start_of_range=90.0, end_of_range=100.0  # Maintain high charge
                        ),
                    ),
                ],
            )
        )
        time.sleep(5)
        print("Send storage status - current charge level")
        conn.send_msg_and_await_reception_status_sync(
            FRBCStorageStatus(message_id=uuid.uuid4(), present_fill_level=20.0)  # Start at 20% like example
        )
        time.sleep(5)
        print("Send actuator status - currently in charge mode")
        conn.send_msg_and_await_reception_status_sync(
            FRBCActuatorStatus(
                message_id=uuid.uuid4(),
                actuator_id=actuator_id,
                active_operation_mode_id=charge_operation_mode_id,  # Start in charge mode
                operation_mode_factor=0.0,  # Will be set by CEM instructions
            )
        )

        # Start the countdown loop for sending periodic actuator status
        self._start_actuator_status_loop(conn, actuator_id, charge_operation_mode_id)

    def _start_actuator_status_loop(self, conn: S2Connection, actuator_id: uuid.UUID, operation_mode_id: uuid.UUID) -> None:
        """Start a background thread that sends actuator status every 45 seconds with countdown display."""
        def countdown_and_send():
            while True:
                try:
                    # 45 second countdown with display
                    for remaining in range(20, 0, -1):
                        print(f"\rNext actuator status in {remaining:2d} seconds...", end="", flush=True)
                        time.sleep(1)
                    
                    print("\rSending actuator status...                    ")
                    
                    # Send actuator status
                    conn.send_msg_and_await_reception_status_sync(
                        FRBCActuatorStatus(
                            message_id=uuid.uuid4(),
                            actuator_id=actuator_id,
                            active_operation_mode_id=operation_mode_id,
                            operation_mode_factor=0.0,
                        )
                    )
                    print("Actuator status sent successfully!")
                    
                except Exception as e:
                    print(f"\nError sending actuator status: {e}")
                    break
        
        # Start the countdown thread as daemon so it stops when main program exits
        countdown_thread = threading.Thread(target=countdown_and_send, daemon=True)
        countdown_thread.start()

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


def start_s2_session(url, client_node_id=str(uuid.uuid4()), bearer_token=None):
    s2_conn = S2Connection(
        url=url,
        role=EnergyManagementRole.RM,
        control_types=[MyFRBCControlType(), MyNoControlControlType()],
        asset_details=AssetDetails(
            resource_id=client_node_id,
            name="Some asset",
            instruction_processing_delay=Duration.from_milliseconds(20),
            roles=[
                Role(role=RoleType.ENERGY_CONSUMER, commodity=Commodity.ELECTRICITY)
            ],
            currency=Currency.EUR,
            provides_forecast=False,
            provides_power_measurements=[CommodityQuantity.ELECTRIC_POWER_L1],
        ),
        reconnect=True,
        verify_certificate=False,
        bearer_token=bearer_token,
    )

    # Create signal handlers
    def sigint_handler(signum, frame):
        stop(s2_conn, signum, frame)

    def sigterm_handler(signum, frame):
        stop(s2_conn, signum, frame)

    # Register signal handlers
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)

    s2_conn.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple S2 resource manager example."
    )
    parser.add_argument(
        "--endpoint",
        type=str,
        help="WebSocket endpoint uri for the server (CEM) e.g. "
        "ws://localhost:8080/",
    )
    parser.add_argument(
        "--resource-id",
        type=str,
        required=False,
        help="Resource that we want to manage. "
             "Some UUID",
    )
    parser.add_argument(
        "--bearer-token",
        type=str,
        required=False,
        help="Bearer token for testing."
    )
    args = parser.parse_args()
    args.bearer_token = 'cvp6XXTsgonYda9IB52ltqS+StG7xFrt+ApqVIwUVhg='
    # Use provided resource_id or generate a new UUID if None
    resource_id = args.resource_id if args.resource_id is not None else str(uuid.uuid4())
    start_s2_session(args.endpoint, resource_id, args.bearer_token)
