import abc

from s2python.generated.gen_s2_pairing import ConnectionDetails, ConnectionRequest, PairingResponse, PairingRequest


class S2AbstractServer(abc.ABC):
    """Abstract server for handling S2 protocol pairing and connections.

    This class serves as an interface that developers can extend to implement
    S2 protocol functionality with their preferred technology stack.
    Concrete implementations should override the abstract methods marked
    with @abc.abstractmethod.
    """

    @abc.abstractmethod
    def handle_pairing_request(self, request_data: PairingRequest) -> PairingResponse:
        pass

    @abc.abstractmethod
    def handle_connection_request(self, request_data: ConnectionRequest) -> ConnectionDetails:
        pass
