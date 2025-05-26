"""
Default implementation of the S2 protocol server.
"""

import base64
import http.server
import json
import logging
import socketserver
import asyncio
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional

from jwskate import Jwk, Jwt
from jwskate.jwe.compact import JweCompact
import websockets

from s2python.authorization.server import S2AbstractServer
from s2python.generated.gen_s2_pairing import (
    ConnectionDetails,
    ConnectionRequest,
    PairingRequest,
    PairingResponse,
    Protocols,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("S2DefaultServer")


class S2DefaultHTTPHandler(http.server.BaseHTTPRequestHandler):
    """Default HTTP handler for S2 protocol server."""

    def __init__(self, *args: Any, server_instance: Any = None, **kwargs: Any) -> None:
        """Initialize the handler with server instance."""
        self.server_instance = server_instance
        super().__init__(*args, **kwargs)

    def do_POST(self) -> None:  # pylint: disable=C0103
        """Handle POST requests for pairing and connection."""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")

        try:
            request_json = json.loads(post_data)
            logger.info("Received request at %s", self.path)
            logger.debug("Request body: %s", request_json)

            if self.path == "/requestPairing":
                self._handle_pairing_request(request_json)
            elif self.path == "/requestConnection":
                self._handle_connection_request(request_json)
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
                logger.error("Unknown endpoint: %s", self.path)

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            logger.error("Error handling request: %s", e)
            raise e

    def _handle_pairing_request(self, request_json: Dict[str, Any]) -> None:
        """Handle a pairing request.

        Args:
            request_json: The JSON request body
        """
        try:
            # Convert request to PairingRequest
            pairing_request = PairingRequest.model_validate(request_json)

            # Process request using server instance
            response = self.server_instance.handle_pairing_request(pairing_request)

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response.model_dump_json().encode())
            logger.info("Pairing request successful")

        except ValueError as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            logger.error("Invalid pairing request: %s", e)

    def _handle_connection_request(self, request_json: Dict[str, Any]) -> None:
        """Handle a connection request.

        Args:
            request_json: The JSON request body
        """
        try:
            # Convert request to ConnectionRequest
            connection_request = ConnectionRequest.model_validate(request_json)

            # Process request using server instance
            response = self.server_instance.handle_connection_request(connection_request)

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response.model_dump_json().encode())
            logger.info("Connection request successful")

        except ValueError as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            logger.error("Invalid connection request: %s", e)

    def log_message(self, format: str, *args: Any) -> None:  # pylint: disable=W0622
        """Log messages using the logger instead of printing to stderr."""
        logger.info(format % args)  # pylint: disable=W1201


class S2DefaultServer(S2AbstractServer):
    """Default implementation of the S2 protocol server using http.server."""

    def __init__(
        self,
        host: str = "localhost",
        http_port: int = 8000,
        ws_port: int = 8080,
        instance: str = "http",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the default server implementation.

        Args:
            host: The host to bind to
            http_port: The HTTP port to use
            ws_port: The WebSocket port to use
        """
        super().__init__(*args, **kwargs)
        self.host = host
        self.http_port = http_port
        self.ws_port = ws_port
        self._httpd: Optional[socketserver.TCPServer] = None
        self._ws_server: Optional[websockets.serve] = None
        self.instance = instance

    async def _handle_websocket_connection(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        client_id = str(uuid.uuid4())
        logger.info("Client %s connected on path: %s", client_id, path)

        try:
            # Send handshake message to client
            handshake = {
                "type": "Handshake",
                "messageId": str(uuid.uuid4()),
                "protocolVersion": "0.0.2-beta",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            await websocket.send(json.dumps(handshake))
            logger.info("Sent handshake to client %s", client_id)

            # Listen for messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    logger.info("Received message from client %s: %s", client_id, data)

                    # Extract message type
                    message_type = data.get("type", "")
                    message_id = data.get("messageId", str(uuid.uuid4()))

                    # Send reception status
                    reception_status = {
                        "type": "ReceptionStatus",
                        "messageId": str(uuid.uuid4()),
                        "refMessageId": message_id,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "status": "OK",
                    }
                    await websocket.send(json.dumps(reception_status))
                    logger.info("Sent reception status for message %s", message_id)

                    # Handle specific message types
                    if message_type == "HandshakeResponse":
                        logger.info("Received handshake response")

                    # For FRBC messages, you could add specific handling here

                except json.JSONDecodeError:
                    logger.error("Invalid JSON received from client %s", client_id)
                except Exception as e:
                    logger.error("Error processing message from client %s: %s", client_id, e)
                    raise e

        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection with client %s closed", client_id)
        except Exception as e:
            logger.error("Error with client %s: %s", client_id, e)
            raise e
        finally:
            logger.info("Client %s disconnected", client_id)

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

    def _create_signed_token(self, claims: Dict[str, Any], expiry_date: datetime) -> str:
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
        self, client_public_key: str, client_node_id: str, nested_signed_token: str, expiry_date: datetime
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
        # test the decryption of the JWE
        # decrypted_payload = jwe.decrypt(client_jwk)
        # logger.info("Original payload: %s", jwe)
        # logger.info("Decrypted payload: %s", decrypted_payload)

        logger.info("JWE: %s", str(jwe))
        # try to decrypt the JWE
        return str(jwe)

    def start_server(self) -> None:
        """Start the HTTP server."""
        if self.instance == "http":
            self.start_http_server()
        elif self.instance == "ws":
            self.start_ws_server()
        else:
            raise ValueError("Invalid instance type")

    def start_http_server(self) -> None:
        """Start the HTTP server."""

        # Create handler class with server instance
        def handler_factory(*args: Any, **kwargs: Any) -> S2DefaultHTTPHandler:
            return S2DefaultHTTPHandler(*args, server_instance=self, **kwargs)

        # Create and start server
        self._httpd = socketserver.TCPServer((self.host, self.http_port), handler_factory)
        logger.info("S2 Server running at: http://%s:%s", self.host, self.http_port)
        # Start the WebSocket server
        self.start_ws_server()
        self._httpd.serve_forever()

    def stop_server(self) -> None:
        """Stop the HTTP server."""
        if self._httpd:
            # self._httpd.shutdown()
            self._httpd.server_close()
            self._httpd = None
        
    def start_ws_server(self) -> None:
        """Start the WebSocket server."""
        self._ws_server = websockets.serve(self._handle_websocket_connection, self.host, self.ws_port)
        logger.info("S2 WebSocket server running at: ws://%s:%s", self.host, self.ws_port)
        asyncio.get_event_loop().run_until_complete(self._ws_server)
        asyncio.get_event_loop().run_forever()

    def _get_base_url(self) -> str:
        """Get the base URL for the server.

        Returns:
            str: The base URL (e.g., "http://localhost:8000")
        """
        return f"http://{self.host}:{self.http_port}"

    def _get_ws_url(self) -> str:
        """Get the WebSocket URL for the server.

        Returns:
            str: The WebSocket URL
        """
        return f"ws://{self.host}:{self.ws_port}"
