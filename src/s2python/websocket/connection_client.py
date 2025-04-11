from abc import ABC, abstractmethod
from typing import Any, Dict

class AbstractConnectionClient(ABC):
    """Abstract class for handling the /requestConnection endpoint."""

    def request_connection(self) -> Any:
        """Orchestrate the connection request flow: build → execute → handle."""
        request_data = self.build_connection_request()
        response_data = self.execute_connection_request(request_data)
        return self.handle_connection_response(response_data)

    @abstractmethod
    def build_connection_request(self) -> Dict:
        """
        Build the payload for the ConnectionRequest schema.
        Returns a dictionary with keys: s2ClientNodeId, supportedProtocols.
        """
        pass

    @abstractmethod
    def execute_connection_request(self, request_data: Dict) -> Dict:
        """
        Execute the POST request to /requestConnection.
        Implementations should send the request_data to the endpoint
        and return the JSON response as a dictionary.
        """
        pass

    @abstractmethod
    def handle_connection_response(self, response_data: Dict) -> Any:
        """
        Process the ConnectionDetails response (e.g., extract challenge and connection URI).
        The response_data contains keys: selectedProtocol, challenge, connectionUri.
        """
        pass
