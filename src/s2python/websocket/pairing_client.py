from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractPairingClient(ABC):
    """Abstract class for handling the /requestPairing endpoint."""

    def request_pairing(self) -> Any:
        """Orchestrate the pairing request flow: build → execute → handle."""
        request_data = self.build_pairing_request()
        response_data = self.execute_pairing_request(request_data)
        return self.handle_pairing_response(response_data)

    @abstractmethod
    def build_pairing_request(self) -> Dict:
        """
        Build the payload for the PairingRequest schema.
        Returns a dictionary with keys: token, publicKey, s2ClientNodeId,
        s2ClientNodeDescription, supportedProtocols.
        """
        pass

    @abstractmethod
    def execute_pairing_request(self, request_data: Dict) -> Dict:
        """
        Execute the POST request to /requestPairing.
        Implementations should send the request_data to the endpoint
        and return the JSON response as a dictionary.
        """
        pass

    @abstractmethod
    def handle_pairing_response(self, response_data: Dict) -> Any:
        """
        Process the PairingResponse (e.g., extract server details).
        The response_data contains keys: s2ServerNodeId, serverNodeDescription, requestConnectionUri.
        """
        pass
