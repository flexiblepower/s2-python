import http.server
import socketserver
import json
from typing import Any
import uuid
from urllib.parse import urlparse, parse_qs
import ssl
import threading
import logging
import random
import string

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mock_s2_server")


def generate_token() -> str:
    """
    Generate a random alphanumeric token with exactly 32 characters.

    Returns:
        str: A string of 32 random alphanumeric characters matching pattern ^[0-9a-zA-Z]{32}$
    """
    # Define the character set: uppercase letters, lowercase letters, and digits
    chars = string.ascii_letters + string.digits

    # Generate a 32-character token by randomly selecting from the character set
    token = "".join(random.choice(chars) for _ in range(32))

    return token


# Generate random token for pairing
PAIRING_TOKEN = generate_token()
SERVER_NODE_ID = str(uuid.uuid4())
WS_PORT = 8080
HTTP_PORT = 8000


class MockS2Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")

        try:
            request_json = json.loads(post_data)
            logger.info(f"Received request at {self.path} ")
            # logger.info(f"Request body: {request_json}")

            if self.path == "/requestPairing":
                # Handle pairing request
                # The token in the S2 protocol is a PairingToken object with a token field
                token_obj = request_json.get("token", {})

                # Handle case where token is directly the string or a dict with token field
                if isinstance(token_obj, dict) and "token" in token_obj:
                    request_token_string = token_obj["token"]
                else:
                    request_token_string = token_obj

                logger.info(f"Extracted token: {request_token_string}")
                logger.info(f"Expected token: {PAIRING_TOKEN}")

                if request_token_string == PAIRING_TOKEN:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()

                    # Create pairing response
                    response = {
                        "s2ServerNodeId": SERVER_NODE_ID,
                        "serverNodeDescription": {
                            "brand": "Mock S2 Server",
                            "type": "Test Server",
                            "modelName": "Mock Model",
                            "logoUri": "http://example.com/logo.png",
                            "userDefinedName": "Mock Server",
                            "role": "CEM",
                            "deployment": "LAN",
                        },
                        "requestConnectionUri": f"http://localhost:{HTTP_PORT}/requestConnection",
                    }

                    self.wfile.write(json.dumps(response).encode())
                    logger.info("Pairing request successful")
                else:
                    self.send_response(401)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid token"}).encode())
                    logger.error("Invalid pairing token")

            elif self.path == "/requestConnection":
                # Handle connection request
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                # Create challenge (normally would be a JWE)
                challenge = "mock_challenge_string"

                # Create connection details response
                response = {
                    "connectionUri": f"ws://localhost:{WS_PORT}/s2/mock-websocket",
                    "challenge": challenge,
                }

                self.wfile.write(json.dumps(response).encode())
                logger.info("Connection request successful")

            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
                logger.error(f"Unknown endpoint: {self.path}")

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            logger.error(f"Error handling request: {e}")

    def log_message(self, format: str, *args: Any) -> None:
        logger.info(format % args)


def run_server() -> None:
    with socketserver.TCPServer(("localhost", HTTP_PORT), MockS2Handler) as httpd:
        logger.info(f"Mock S2 Server running at http://localhost:{HTTP_PORT}")
        logger.info(f"Use pairing token: {PAIRING_TOKEN}")
        logger.info(f"Pairing endpoint: http://localhost:{HTTP_PORT}/requestPairing")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
