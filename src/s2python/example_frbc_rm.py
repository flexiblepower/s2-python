import uuid

from s2python.common import EnergyManagementRole, Duration, Role, RoleType, Commodity, Currency
from s2python.frbc import FRBCInstruction, FRBCSystemDescription
from s2python.s2_connection import S2Connection, AssetDetails
from s2python.s2_control_type import FRBCControlType


class MyFRBCControlType(FRBCControlType):
    def handle_instruction(self, conn: S2Connection, msg: FRBCInstruction) -> None:
        print(f"I have received the message {msg} from {conn}")

    def activate(self) -> None:
        print("It is now activated.")

    def deactivate(self) -> None:
        print("It is now deactivated.")


s2_conn = S2Connection(
    url="http://cem_is_here.com:8080/",
    role=EnergyManagementRole.RM,
    control_types=[MyFRBCControlType()],
    asset_details=AssetDetails(
        resource_id=str(uuid.uuid4()),
        name="Some asset",
        instruction_processing_delay=Duration.from_milliseconds(20),
        roles=[Role(role=RoleType.ENERGY_CONSUMER, commodity=Commodity.ELECTRICITY)],
        currency=Currency.EUR,
    ),
)

s2_conn.start_as_rm()
s2_conn.send_msg_and_await_reception_status(FRBCSystemDescription(...))
