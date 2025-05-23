"""
Example S2 server implementation.
"""

import argparse
import logging
import signal
import sys
from datetime import datetime, timedelta
from typing import Any

from s2python.authorization.default_server import S2DefaultServer
from s2python.generated.gen_s2_pairing import (
    S2NodeDescription,
    Deployment,
    PairingToken,
    S2Role,
    Protocols,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("example_s2_server")


def signal_handler(sig: int, frame: Any) -> None:
    """Handle Ctrl+C to gracefully shut down the server."""
    logger.info("Shutting down server...")
    if server:
        server.stop_server()
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example S2 server implementation.")
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host to bind the server to (default: localhost)",
    )
    parser.add_argument(
        "--http-port",
        type=int,
        default=8000,
        help="HTTP port to use (default: 8000)",
    )
    parser.add_argument(
        "--ws-port",
        type=int,
        default=8080,
        help="WebSocket port to use (default: 8080)",
    )
    parser.add_argument(
        "--pairing-token",
        type=str,
        default="ca14fda4",
        help="Pairing token to use (default: ca14fda4)",
    )
    args = parser.parse_args()

    # Create node description for the server
    server_node_description = S2NodeDescription(
        brand="TNO",
        logoUri="https://www.tno.nl/publish/pages/5604/tno-logo-1484x835_003_.jpg",
        type="demo frbc example",
        modelName="S2 server example",
        userDefinedName="TNO S2 server example for frbc",
        role=S2Role.RM,
        deployment=Deployment.LAN,
    )

    # Create and configure the server
    server = S2DefaultServer(
        host=args.host,
        http_port=args.http_port,
        ws_port=args.ws_port,
        server_node_description=server_node_description,
        token=PairingToken(token=args.pairing_token),
        supported_protocols=[Protocols.WebSocketSecure],
    )

    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Start the server
    logger.info("Starting S2 server...")
    logger.info("Server will be available at: http://%s:%s", args.host, args.http_port)
    logger.info("Pairing token: %s", args.pairing_token)
    server.start_server()
