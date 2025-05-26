"""
S2 protocol server for handling pairing and secure connections.
"""

import abc
import base64
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List, Union, Tuple

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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("S2AbstractServer")


class S2AbstractServer(abc.ABC):
    """Abstract server for handling S2 protocol pairing and connections.

    Server handles:
    - HTTP server with TLS
    - Storage of client public keys
    - Challenge generation
    - Token validation

    This class serves as an interface that developers can extend to implement
    S2 protocol functionality with their preferred technology stack.
    Concrete implementations should override the abstract methods marked
    with @abc.abstractmethod.
    """

    def __init__(
        self,
        server_node_id: Optional[uuid.UUID] = None,
        server_node_description: Optional[S2NodeDescription] = None,
        token: Optional[PairingToken] = None,
        verify_certificate: Union[bool, str] = False,
        supported_protocols: Optional[List[Protocols]] = None,
    ) -> None:
        """Initialize the server with configuration parameters.

        Args:
            server_node_id: Server node UUID
            server_node_description: S2 node description
            token: Pairing token for authentication
            verify_certificate: Whether to verify SSL certificates (or path to CA cert)
            supported_protocols: List of supported protocols
        """
        # Server configuration
        self.server_node_id = server_node_id if server_node_id else uuid.uuid4()
        self.server_node_description = server_node_description
        self.token = token
        self.verify_certificate = verify_certificate
        self.supported_protocols = supported_protocols or [Protocols.WebSocketSecure]

        # Internal state
        self._client_keys: Dict[str, str] = {}  # client_node_id -> public_key
        self._private_key: Optional[str] = None
        self._private_jwk: Optional[Jwk] = None

    @abc.abstractmethod
    def generate_key_pair(self) -> Tuple[str, str]:
        """Generate a public/private key pair for the server.

        This method should be implemented by concrete subclasses to use their
        preferred cryptographic libraries or key management systems.

        Returns:
            Tuple[str, str]: (public_key, private_key) pair as base64 encoded strings
        """

    @abc.abstractmethod
    def store_key_pair(self, public_key: str, private_key: str) -> None:
        """Store the server's public/private key pair.

        This method should be implemented by concrete subclasses to store keys
        according to their security requirements (e.g., secure storage, HSM, etc.).

        Args:
            public_key: Base64 encoded public key
            private_key: Base64 encoded private key
        """

    def store_client_public_key(self, client_node_id: str, public_key: str) -> None:
        """Store a client's public key.

        Args:
            client_node_id: The client's node ID
            public_key: The client's public key
        """
        self._client_keys[client_node_id] = public_key

    def get_client_public_key(self, client_node_id: str) -> Optional[str]:
        """Get a client's stored public key.

        Args:
            client_node_id: The client's node ID

        Returns:
            Optional[str]: The client's public key if found, None otherwise
        """
        return self._client_keys.get(client_node_id)

    def get_base_url(self) -> str:
        """Get the base URL for the server.

        Returns:
            str: The base URL (e.g., "http://localhost:8000")
        """
        # This should be overridden by concrete implementations
        return "http://localhost:8000"

    def handle_pairing_request(self, pairing_request: PairingRequest) -> PairingResponse:
        """Handle a pairing request from a client.

        Args:
            pairing_request: The pairing request from the client

        Returns:
            PairingResponse: The server's response to the pairing request

        Raises:
            ValueError: If required fields are missing or token is invalid
        """
        logger.info(f"Pairing request for Client Node: {pairing_request}")

        # Validate required fields
        if not pairing_request.publicKey or not pairing_request.s2ClientNodeId or not pairing_request.token:
            raise ValueError("Missing fields, public key, s2ClientNodeId and token are required")

        # Validate token
        # TODO: Get token from server FM
        if not self.token or str(self.token) != str(pairing_request.token):
            raise ValueError("Pairing token provided was not valid")

        # Store client's public key
        # TODO: Store client's public key. sqlLite?
        self.store_client_public_key(str(pairing_request.s2ClientNodeId), pairing_request.publicKey)

        # Create full URLs for endpoints
        base_url = self.get_base_url()
        request_connection_uri = f"{base_url}/requestConnection"
        logger.info(f"Request connection URI: {request_connection_uri}")
        # Create pairing response
        pairing_response = PairingResponse(
            s2ServerNodeId=str(self.server_node_id),
            serverNodeDescription=self.server_node_description,
            requestConnectionUri=request_connection_uri,
        )

        logger.info(f"Pairing response: {pairing_response}")
        return pairing_response

    def handle_connection_request(self, connection_request: ConnectionRequest) -> ConnectionDetails:
        """Handle a connection request from a client.

        Args:
            connection_request: The connection request from the client

        Returns:
            ConnectionDetails: The connection details for the client

        Raises:
            ValueError: If protocol is not supported or client key is not found
        """
        logger.info(f"Connection request: {connection_request}")

        # Validate supported protocols
        if (
            not connection_request.supportedProtocols
            or Protocols.WebSocketSecure not in connection_request.supportedProtocols
        ):
            raise ValueError("S2 Server does not support any of the protocols supported by the client")

        # Get client's public key
        client_public_key = self.get_client_public_key(connection_request.s2ClientNodeId)
        if not client_public_key:
            raise ValueError("Cannot retrieve client's public key")

        # Generate challenge
        expiry_date = datetime.utcnow() + timedelta(minutes=5)

        # Create nested signed token
        nested_signed_token = self._create_signed_token(
            claims={"S2ClientNodeId": connection_request.s2ClientNodeId}, expiry_date=expiry_date
        )

        # Create encrypted challenge
        challenge = self._create_encrypted_challenge(
            client_public_key, connection_request.s2ClientNodeId, nested_signed_token, expiry_date
        )
       
        # Create connection details
        connection_details = ConnectionDetails(
            selectedProtocol=Protocols.WebSocketSecure,
            challenge=challenge,
            connectionUri="/ws",  # This should be configurable
        )

        logger.info(f"Connection details: {connection_details}")
        return connection_details

    @abc.abstractmethod
    def _create_signed_token(self, claims: Dict[str, Any], expiry_date: datetime) -> str:
        """Create a signed JWT token.

        Args:
            claims: The claims to include in the token
            expiry_date: The token's expiration date

        Returns:
            str: The signed JWT token
        """

    @abc.abstractmethod
    def _create_encrypted_challenge(
        self, client_public_key: str, client_node_id: str, nested_signed_token: str, expiry_date: datetime
    ) -> Any:
        """Create an encrypted challenge for the client.
            TODO: using Any to avoid stringification of the JWE. Pros/Cons?
        Args:
            client_public_key: The client's public key
            client_node_id: The client's node ID
            nested_signed_token: The nested signed token
            expiry_date: The challenge's expiration date

        Returns:
            str: The encrypted challenge
        """

    @abc.abstractmethod
    def start_server(self) -> None:
        """Start the server.

        This method should be implemented by concrete subclasses to start
        the server using their preferred web framework.
        """

    @abc.abstractmethod
    def stop_server(self) -> None:
        """Stop the server.

        This method should be implemented by concrete subclasses to stop
        the server gracefully.
        """
