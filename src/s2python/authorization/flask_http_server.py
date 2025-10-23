"""
Flask implementation of the S2 protocol server.
"""

import logging
from datetime import datetime
from typing import Dict, Any, Tuple
import json

from flask import Flask, request
from jwskate import Jwk, Jwt
from jwskate.jwe.compact import JweCompact

from s2python.authorization.server import S2AbstractServer
from s2python.generated.gen_s2_pairing import (
    ConnectionRequest,
    PairingRequest,
)

from s2python.communication.s2_connection import MessageHandlers, S2Connection
from s2python.s2_parser import S2Parser

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("S2FlaskServer")


class S2FlaskHTTPServer(S2AbstractServer):
    """Flask implementation of the S2 protocol server."""

    def __init__(
        self,
        host: str = "localhost",
        http_port: int = 8000,
        ws_port: int = 8080,
        instance: str = "http",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the Flask server implementation.

        Args:
            host: The host to bind to
            http_port: The HTTP port to use
            ws_port: The WebSocket port to use
            instance: The instance type (http or ws)
        """
        super().__init__(*args, **kwargs)
        self.host = host
        self.http_port = http_port
        self.ws_port = ws_port
        self.instance = instance
        self._app = Flask(__name__)
        self._connections: Dict[str, S2Connection] = {}
        self._handlers = MessageHandlers()
        self.s2_parser = S2Parser()
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up Flask routes for the server."""
        self._app.add_url_rule(
            "/requestPairing",
            "requestPairing",
            self._handle_pairing_request,
            methods=["POST"],
        )
        self._app.add_url_rule(
            "/requestConnection",
            "requestConnection",
            self._handle_connection_request,
            methods=["POST"],
        )

    def _handle_pairing_request(self) -> Tuple[dict, int]:
        """Handle a pairing request.

        Returns:
            Tuple[dict, int]: (response JSON, status code)
        """
        try:
            request_json = request.get_json()
            logger.info("Received pairing request at /requestPairing")
            logger.debug("Request body: %s", request_json)

            # Convert request to PairingRequest
            pairing_request = PairingRequest.model_validate(request_json)

            # Process request using server instance
            response = self.handle_pairing_request(pairing_request)

            # Send response
            logger.info("Pairing request successful")
            return response.model_dump(), 200

        except ValueError as e:
            logger.error("Invalid pairing request: %s", e)
            return {"error": str(e)}, 400
        except Exception as e:
            logger.error("Error handling pairing request: %s", e)
            return {"error": str(e)}, 500

    def _handle_connection_request(self) -> Tuple[dict, int]:
        """Handle a connection request.

        Returns:
            Tuple[dict, int]: (response JSON, status code)
        """
        try:
            request_json = request.get_json()
            logger.info("Received connection request at /requestConnection")
            logger.debug("Request body: %s", request_json)

            # Convert request to ConnectionRequest
            connection_request = ConnectionRequest.model_validate(request_json)

            # Process request using server instance
            response = self.handle_connection_request(connection_request)

            # Send response
            logger.info("Connection request successful")
            return response.model_dump(), 200

        except ValueError as e:
            logger.error("Invalid connection request: %s", e)
            return {"error": str(e)}, 400
        except Exception as e:
            logger.error("Error handling connection request: %s", e)
            return {"error": str(e)}, 500

    def generate_key_pair(self) -> Tuple[str, str]:
        """Generate a public/private key pair for the server.

        Returns:
            Tuple[str, str]: (public_key, private_key) pair as base64 encoded strings
        """
        logger.info("Generating key pair")
        self._key_pair = Jwk.generate_for_alg("RSA-OAEP-256").with_kid_thumbprint()
        self._public_jwk = self._key_pair
        self._private_jwk = self._key_pair
        return (
            self._public_jwk.to_pem(),
            self._private_jwk.to_pem(),
        )

    def store_key_pair(self, public_key: str, private_key: str) -> None:
        """Store the server's public/private key pair.

        Args:
            public_key: Base64 encoded public key
            private_key: Base64 encoded private key
        """
        self._private_key = private_key
        # Convert to JWK for JWT operations
        self._private_jwk = Jwk.from_pem(private_key)

    def _create_signed_token(
        self, claims: Dict[str, Any], expiry_date: datetime
    ) -> str:
        """Create a signed JWT token.

        Args:
            claims: The claims to include in the token
            expiry_date: The token's expiration date

        Returns:
            str: The signed JWT token
        """
        if not self._private_jwk:
            # Generate key pair with correct algorithm
            self._key_pair = Jwk.generate_for_alg("RS256").with_kid_thumbprint()
            self._private_jwk = self._key_pair
            self._public_jwk = self._key_pair

        # Add expiration to claims
        claims["exp"] = int(expiry_date.timestamp())

        # Create JWT with claims using RS256 for signing
        token = Jwt.sign(claims=claims, key=self._private_jwk, alg="RS256")

        return str(token)

    def _create_encrypted_challenge(
        self,
        client_public_key: str,
        client_node_id: str,
        nested_signed_token: str,
        expiry_date: datetime,
    ) -> str:
        """Create an encrypted challenge for the client.

        Args:
            client_public_key: The client's public key
            client_node_id: The client's node ID
            nested_signed_token: The nested signed token
            expiry_date: The challenge's expiration date

        Returns:
            str: The encrypted challenge
        """
        # Convert client's public key to JWK
        client_jwk = Jwk.from_pem(client_public_key)

        # Create the payload to encrypt - this will be decrypted and used as an unprotected JWT
        payload = {
            "S2ClientNodeId": client_node_id,
            "signedToken": nested_signed_token,
            "exp": int(expiry_date.timestamp()),
        }

        # Create JWE with all required components
        jwe = JweCompact.encrypt(
            plaintext=json.dumps(payload).encode(),
            key=client_jwk,  # Using client's public key for encryption
            alg="RSA-OAEP-256",
            enc="A256GCM",
        )

        logger.info("JWE: %s", str(jwe))
        return str(jwe)

    def start_server(self) -> None:
        """Start the HTTP or WebSocket server."""
        if self.instance == "http":
            logger.info("Starting Flask HTTP server------>")
            self._app.run(host=self.host, port=self.http_port)
        else:
            raise ValueError("Invalid instance type")

    def stop_server(self) -> None:
        """Stop the server."""
        # Flask doesn't have a built-in way to stop the server
        # This would typically be handled by the WSGI server
        pass

    def _get_ws_url(self) -> str:
        """Get the WebSocket URL for the server."""
        return f"ws://{self.host}:{self.ws_port}"

    def _get_base_url(self) -> str:
        """Get the base URL for the server.

        Returns:
            str: The base URL (e.g., "http://localhost:8000")
        """
        return f"http://{self.host}:{self.http_port}"
