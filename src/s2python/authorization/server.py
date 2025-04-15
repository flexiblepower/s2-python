from abc import ABC, abstractmethod

from s2python.generated.gen_s2_pairing import ConnectionDetails, ConnectionRequest, PairingResponse, PairingRequest


class AbstractAuthServer(ABC):

    @abstractmethod
    def handle_pairing_request(self, request_data: PairingRequest) -> PairingResponse:
        pass

    @abstractmethod
    def handle_connection_request(self, request_data: ConnectionRequest) -> ConnectionDetails:
        pass
