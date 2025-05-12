"""
S2 protocol client for handling pairing and secure connections.
"""

import abc
import json
import uuid
import datetime
import logging
from typing import Dict, Optional, Tuple, Union, List, Any


from jwskate import Jwk
from pydantic import BaseModel

from s2python.generated.gen_s2_pairing import (
    ConnectionDetails,
    ConnectionRequest,
    PairingRequest,
    PairingResponse,
    PairingToken,
    S2NodeDescription,
    Protocols,
)


REQTEST_TIMEOUT = 10
PAIRING_TIMEOUT = datetime.timedelta(minutes=5)
KEY_ALGORITHM = "RSA-OAEP-256"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("S2AbstractClient")

class PairingDetails(BaseModel):
    """Contains all details from the pairing process."""

    pairing_response: PairingResponse
    connection_details: ConnectionDetails
    decrypted_challenge_str: Optional[str] = None


class S2AbstractClient(abc.ABC):
    """Abstract client for handling S2 protocol pairing and connections.

    Client handles:
    - HTTP client with TLS
    - Storage of connection request URI
    - Storage of public/private key pairs
    - Challenge solving

    This class serves as an interface that developers can extend to implement
    S2 protocol functionality with their preferred technology stack.
    Concrete implementations should override the abstract methods marked
    with @abc.abstractmethod.
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        pairing_uri: Optional[str] = None,
        token: Optional[PairingToken] = None,
        node_description: Optional[S2NodeDescription] = None,
        verify_certificate: Union[bool, str] = False,
        client_node_id: Optional[uuid.UUID] = None,
        supported_protocols: Optional[List[Protocols]] = None,
    ) -> None:
        """Initialize the client with configuration parameters.

        Args:
            pairing_uri: URI for the pairing request
            token: Pairing token for authentication
            node_description: S2 node description
            verify_certificate: Whether to verify SSL certificates (or path to CA cert)
            client_node_id: Client node UUID (generated if not provided)
            supported_protocols: List of supported protocols
        """
        # Connection and authentication info
        self.pairing_uri = pairing_uri
        self.token = token
        self.node_description = node_description
        self.verify_certificate = verify_certificate
        self.client_node_id = client_node_id if client_node_id else uuid.uuid4()
        self.supported_protocols = supported_protocols or [Protocols.WebSocketSecure]

        # Internal state
        self._connection_request_uri: Optional[str] = None
        self._public_key: Optional[str] = None
        self._private_key: Optional[str] = None
        self._public_jwk: Optional[Jwk] = None
        self._private_jwk: Optional[Jwk] = None
        self._key_pair: Optional[Jwk] = None
        self._pairing_response: Optional[PairingResponse] = None
        self._connection_details: Optional[ConnectionDetails] = None
        self._pairing_details: Optional[PairingDetails] = None

    @property
    def connection_request_uri(self) -> Optional[str]:
        """Get the stored connection request URI."""
        return self._connection_request_uri

    def store_connection_request_uri(self, uri: str) -> None:
        """Store the connection request URI.

        If the provided URI is empty, None, or doesn't contain 'requestConnection',
        it will attempt to derive it from the pairing URI by replacing 'requestPairing'
        with 'requestConnection'.

        Args:
            uri: The connection request URI from the pairing response
        """
        if uri is not None and uri.strip() != "" and "requestConnection" in uri:
            self._connection_request_uri = uri
        elif self.pairing_uri is not None and "requestPairing" in self.pairing_uri:
            # Fall back to constructing the URI from the pairing URI
            self._connection_request_uri = self.pairing_uri.replace(
                "requestPairing", "requestConnection"
            )
        else:
            # No valid URI could be determined
            self._connection_request_uri = None

    @abc.abstractmethod
    def generate_key_pair(self) -> Tuple[str, str]:
        """Generate a public/private key pair.

        This method should be implemented by concrete subclasses to use their
        preferred cryptographic libraries or key management systems.

        Returns:
            Tuple[str, str]: (public_key, private_key) pair as base64 encoded strings
        """

    @abc.abstractmethod
    def store_key_pair(self, public_key: str, private_key: str) -> None:
        """Store the public/private key pair.

        This method should be implemented by concrete subclasses to store keys
        according to their security requirements (e.g., secure storage, HSM, etc.).

        Args:
            public_key: Base64 encoded public key
            private_key: Base64 encoded private key
        """

    @abc.abstractmethod
    def _make_https_request(
        self,
        url: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[int, str]:
        """Make an HTTPS request.

        This method should be implemented by concrete subclasses to use their
        preferred HTTP client library or framework.

        Args:
            url: Target URL
            method: HTTP method (GET, POST, etc.)
            data: Request body data
            headers: HTTP headers

        Returns:
            Tuple[int, str]: (status_code, response_text)
        """

    def request_pairing(self) -> PairingResponse:
        """Send a pairing request to the server using client configuration.

        Returns:
            PairingResponse: The server's response to the pairing request

        Raises:
            ValueError: If pairing_uri or token is not set, or if the request fails
        """
        if not self.pairing_uri:
            raise ValueError(
                "Pairing URI not set. Set pairing_uri before calling request_pairing."
            )

        if not self.token:
            raise ValueError(
                "Pairing token not set. Set token before calling request_pairing."
            )

        # Ensure we have keys
        if not self._public_key:
            public_key, private_key = self.generate_key_pair()
            self.store_key_pair(public_key, private_key)

        # Create pairing request
        logger.info("Creating pairing request")
        pairing_request = PairingRequest(
            token=self.token,
            publicKey=self._public_key,
            s2ClientNodeId=str(self.client_node_id),
            s2ClientNodeDescription=self.node_description,
            supportedProtocols=self.supported_protocols,
        )

        # Make pairing request
        logger.info("Making pairing request")
        status_code, response_text = self._make_https_request(
            url=self.pairing_uri,
            method="POST",
            data=pairing_request.model_dump(exclude_none=True),
            headers={"Content-Type": "application/json"},
        )
        logger.info('Pairing request response: %s %s', status_code, response_text)

        # Parse response
        if status_code != 200:
            raise ValueError(
                f"Pairing request failed with status {status_code}: {response_text}"
            )

        pairing_response = PairingResponse.model_validate(json.loads(response_text))

        # Store for later use
        self._pairing_response = pairing_response
        self.store_connection_request_uri(str(pairing_response.requestConnectionUri))

        return pairing_response

    def request_connection(self) -> ConnectionDetails:
        """Request connection details from the server.

        Returns:
            ConnectionDetails: The connection details returned by the server

        Raises:
            ValueError: If connection request URI is not set or if the request fails
        """
        if not self._connection_request_uri:
            raise ValueError(
                "Connection request URI not set. Call request_pairing first."
            )

        # Create connection request
        connection_request = ConnectionRequest(
            s2ClientNodeId=str(self.client_node_id),
            supportedProtocols=self.supported_protocols,
        )

        # Make a POST request to the connection request URI
        status_code, response_text = self._make_https_request(
            url=self._connection_request_uri,
            method="POST",
            data=connection_request.model_dump(exclude_none=True),
            headers={"Content-Type": "application/json"},
        )

        # Parse response
        if status_code != 200:
            raise ValueError(
                f"Connection request failed with status {status_code}: {response_text}"
            )

        connection_details = ConnectionDetails.model_validate(json.loads(response_text))

        # Handle relative WebSocket URI paths
        if (
            connection_details.connectionUri is not None
            and not str(connection_details.connectionUri).startswith("ws://")
            and not str(connection_details.connectionUri).startswith("wss://")
        ):

            # If websocket address doesn't start with ws:// or wss:// assume it's relative to the pairing URI
            if self.pairing_uri:
                base_uri = self.pairing_uri
                # Convert to WebSocket protocol and remove the requestPairing path
                ws_base = (
                    base_uri.replace("http://", "ws://")
                    .replace("https://", "wss://")
                    .replace("requestPairing", "")
                    .rstrip("/")
                )

                # Combine with the relative path from connectionUri
                relative_path = str(connection_details.connectionUri).lstrip("/")

                # Create complete URL
                full_ws_url = f"{ws_base}/{relative_path}"

                try:
                    # Update the connection details with the new URL
                    connection_data = connection_details.model_dump()
                    # Replace the URI with the full WebSocket URL
                    connection_data["connectionUri"] = full_ws_url
                    # Recreate the ConnectionDetails object
                    connection_details = ConnectionDetails.model_validate(
                        connection_data
                    )
                    logger.info('Updated relative WebSocket URI to absolute: %s', full_ws_url)
                except (ValueError, TypeError, KeyError) as e:
                    logger.info('Failed to update WebSocket URI: %s', e)
            else:
                # Log a warning but don't modify the URI if we can't create a proper absolute URI
                logger.info('Received relative WebSocket URI but pairing_uri is not available to create absolute URL')

        # Store for later use
        self._connection_details = connection_details

        return connection_details

    @abc.abstractmethod
    def solve_challenge(self, challenge: Optional[str] = None) -> str:
        """Solve the connection challenge using the public key.

        If no challenge is provided, uses the challenge from connection_details.

        The challenge is a JWE (JSON Web Encryption) that must be decrypted using
        the client's public key, then encoded as a base64 string.

        Args:
            challenge: The challenge string from the server (optional)

        Returns:
            str: The solution to the challenge (base64 encoded decrypted challenge)

        Raises:
            ValueError: If no challenge is provided and connection_details is not set
            ValueError: If the public key is not available
            RuntimeError: If challenge decryption fails
        """

    @abc.abstractmethod
    def establish_secure_connection(self) -> Any:
        """Establish a secure connection to the server.

        This method should be implemented by concrete subclasses to establish
        a secure connection using the connection details and solved challenge.
        Implementations needs to use WebSocket Secure.

        Returns:
            Any: A connection object or handler specific to the implementation

        Raises:
            ValueError: If connection details or solved challenge are not available
            RuntimeError: If connection establishment fails
        """

    @abc.abstractmethod
    def close_connection(self) -> None:
        """Close the connection to the server.

        This method should be implemented by concrete subclasses to properly
        close the connection established by establish_secure_connection.
        """

    @property
    def pairing_details(self) -> Optional[PairingDetails]:
        """Get the stored pairing details."""
        return self._pairing_details
