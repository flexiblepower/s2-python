"""
Default implementation of the S2 protocol client.

This module provides a concrete implementation of the S2AbstractClient
for developers to use directly or as a reference for their own implementations.
"""

import base64
import json
import uuid
import logging
from typing import Dict, Optional, Tuple, Union, List, Any, Mapping

import requests
from requests import Response

from jwskate import JweCompact, Jwk, Jwt

from s2python.generated.gen_s2_pairing import (
    PairingToken,
    S2NodeDescription,
    Protocols,
)
from s2python.authorization.client import (
    S2AbstractClient,
    REQTEST_TIMEOUT,
    KEY_ALGORITHM,
    PairingDetails,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("S2DefaultClient")


class S2DefaultClient(S2AbstractClient):
    """Default implementation of the S2AbstractClient using the requests library for HTTP
    and jwskate for cryptographic operations.

    This implementation can be used directly or as a reference for custom implementations.
    """

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
        """Initialize the default client with configuration parameters."""
        super().__init__(
            pairing_uri,
            token,
            node_description,
            verify_certificate,
            client_node_id,
            supported_protocols,
        )
        # Additional state for this implementation
        self._ws_connection: Optional[Dict[str, Any]] = None

    def generate_key_pair(self) -> Tuple[str, str]:
        """Generate a public/private key pair using jwskate library.

        Returns:
            Tuple[str, str]: (public_key, private_key) pair as PEM encoded strings
        """
        logger.info("Generating key pair")
        self._key_pair = Jwk.generate_for_alg(KEY_ALGORITHM).with_kid_thumbprint()
        self._public_jwk = self._key_pair
        self._private_jwk = self._key_pair
        return (
            self._public_jwk.to_pem(),
            self._private_jwk.to_pem(),
        )

    def store_key_pair(self, public_key: str, private_key: str) -> None:
        """Store the public/private key pair in memory.

        In a production implementation, this might use a secure storage mechanism
        like a keystore, HSM, or encrypted database.

        Args:
            public_key: PEM encoded public key
            private_key: PEM encoded private key
        """
        logger.info("Storing key pair")
        self._public_key = public_key
        self._private_key = private_key

    def _make_https_request(
        self,
        url: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[int, str]:
        """Make an HTTPS request using the requests library.

        Args:
            url: Target URL
            method: HTTP method (GET, POST, etc.)
            data: Request body data
            headers: HTTP headers

        Returns:
            Tuple[int, str]: (status_code, response_text)
        """
        # Using requests library with verification settings from instance
        response: Response = requests.request(
            method=method,
            url=url,
            json=data,
            headers=headers or {"Content-Type": "application/json"},
            verify=self.verify_certificate,
            timeout=REQTEST_TIMEOUT,
        )
        return response.status_code, response.text

    def solve_challenge(self, challenge: Optional[Any] = None) -> str:
        """Solve the connection challenge using the public key.

        If no challenge is provided, uses the challenge from connection_details.

        Args:
            challenge: The challenge string from the server (optional)

        Returns:
            str: The solution to the challenge (base64 encoded decrypted challenge)

        Raises:
            ValueError: If no challenge is provided and connection_details is not set
            ValueError: If the public key is not available
            RuntimeError: If challenge decryption fails
        """
        if challenge is None:
            if not self._connection_details or not self._connection_details.challenge:
                raise ValueError(
                    "Challenge not provided and not available in connection details"
                )
            challenge = self._connection_details.challenge

        if not self._key_pair and not self._public_key:
            raise ValueError(
                "Public key is not available. Generate or load a key pair first."
            )

        try:
            # If we have a jwskate Jwk object, use it directly
            if self._key_pair:
                rsa_key_pair = self._key_pair
            # Otherwise try to parse the public key
            elif self._public_key:
                rsa_key_pair = Jwk.from_pem(self._public_key)
            else:
                raise ValueError("No public key available")
            # check that the challenge is a JweCompact
            if not isinstance(challenge, str):
                raise ValueError("Challenge is not a string")
            # Log the challenge
            # logger.info("Challenge: %s", challenge)

            # Decrypt the JWE challenge - get result as bytes and convert to string
            compact_jwe = JweCompact(challenge)
            # logger.info("Compact JWE: %s", compact_jwe)
            decrypted_bytes = compact_jwe.decrypt(rsa_key_pair)
            # Make sure we have a proper string
            if hasattr(decrypted_bytes, "decode"):
                decrypted_string = decrypted_bytes.decode("utf-8")
            else:
                decrypted_string = str(decrypted_bytes)

            # Parse the JSON payload
            challenge_mapping: Mapping[str, Any] = json.loads(decrypted_string)

            # Create an unprotected JWT from the challenge
            jwt_token = Jwt.unprotected(challenge_mapping)
            jwt_token_str = str(jwt_token)

            # Encode the token as base64
            decrypted_challenge_str: str = base64.b64encode(
                jwt_token_str.encode("utf-8")
            ).decode("utf-8")

            # Store the pairing details if we have all required components
            if self._pairing_response and self._connection_details:
                self._pairing_details = PairingDetails(
                    pairing_response=self._pairing_response,
                    connection_details=self._connection_details,
                    decrypted_challenge_str=decrypted_challenge_str,
                )

            logger.info("Decrypted challenge: %s", decrypted_challenge_str)
            return decrypted_challenge_str

        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as e:
            error_msg = f"Failed to solve challenge: {e}"
            logger.info(error_msg)
            raise RuntimeError(error_msg) from e

    def establish_secure_connection(self) -> Dict[str, Any]:
        """Establish a secure WebSocket connection.

        This implementation establishes a WebSocket connection
        using the connection details and solved challenge.

        Note: This is a placeholder implementation. In a real implementation,
        this would use a WebSocket library like websocket-client or websockets.

        Returns:
            Dict[str, Any]: A WebSocket connection object

        Raises:
            ValueError: If connection details or solved challenge are not available
            RuntimeError: If connection establishment fails
        """
        if not self._connection_details:
            raise ValueError(
                "Connection details not available. Call request_connection first."
            )

        if (
            not self._pairing_details
            or not self._pairing_details.decrypted_challenge_str
        ):
            raise ValueError(
                "Challenge solution not available. Call solve_challenge first."
            )

        logger.info(
            "Establishing WebSocket connection to %s,",
            self._connection_details.connectionUri,
        )
        logger.info(
            "Using solved challenge: %s", self._pairing_details.decrypted_challenge_str
        )

        # Placeholder for the connection object
        self._ws_connection = {
            "status": "connected",
            "uri": str(self._connection_details.connectionUri),
        }

        return self._ws_connection

    def close_connection(self) -> None:
        """Close the WebSocket connection."""
        if self._ws_connection:

            logger.info("Would close WebSocket connection")
            self._ws_connection = None
