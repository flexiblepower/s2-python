import socketserver
import json
from typing import Any
import uuid
import logging
import random
import string

from s2python.authorization.default_server import S2DefaultHTTPHandler

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


class MockS2Handler(S2DefaultHTTPHandler):
    def do_POST(self) -> None:  # pylint: disable=C0103
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")

        try:
            request_json = json.loads(post_data)
            logger.info("Received request at %s", self.path)
            logger.debug("Request body: %s", request_json)

            if self.path == "/requestPairing":
                # Handle pairing request
                # The token in the S2 protocol is a PairingToken object with a token field
                token_obj = request_json.get("token", {})

                # Handle case where token is directly the string or a dict with token field
                if isinstance(token_obj, dict) and "token" in token_obj:
                    request_token_string = token_obj["token"]
                else:
                    request_token_string = token_obj

                logger.info("Extracted token: %s", request_token_string)
                logger.info("Expected token: %s", PAIRING_TOKEN)

                if request_token_string == PAIRING_TOKEN:
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
                    self._send_json_response(200, response)
                    logger.info("Pairing request successful")
                else:
                    self._send_json_response(401, {"error": "Invalid token"})
                    logger.error("Invalid pairing token")

            elif self.path == "/requestConnection":
                # Create challenge (normally would be a JWE)
                challenge = "mock_challenge_string"

                # Create connection details response
                response = {
                    "connectionUri": f"ws://localhost:{WS_PORT}/s2/mock-websocket",
                    "challenge": challenge,
                    "selectedProtocol": "WebSocketSecure",
                }

                # Handle connection request
                self._send_json_response(200, response)
                logger.info("Connection request successful")

            else:
                self._send_json_response(404, {"error": "Endpoint not found"})
                logger.error("Unknown endpoint: %s", self.path)

        except Exception as e:
            self._send_json_response(500, {"error": str(e)})
            logger.error("Error handling request: %s", e)
            raise e

    def log_message(self, format: str, *args: Any) -> None:  # pylint: disable=W0622
        logger.info(format % args)  # pylint: disable=W1201


def run_server() -> None:
    with socketserver.TCPServer(("localhost", HTTP_PORT), MockS2Handler) as httpd:
        logger.info("Mock S2 Server running at: http://localhost:%s", HTTP_PORT)
        logger.info("Use pairing token: %s", PAIRING_TOKEN)
        logger.info("Pairing endpoint: http://localhost:%s/requestPairing", HTTP_PORT)
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
