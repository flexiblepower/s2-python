"""
Example S2 server implementation.
"""

import argparse
import logging
import signal
import sys
from datetime import datetime, timedelta
from typing import Any
import asyncio
import uuid

from s2python.authorization.default_http_server import S2DefaultHTTPServer
from s2python.authorization.default_ws_server import S2DefaultWSServer
from s2python.generated.gen_s2_pairing import (
    S2NodeDescription,
    Deployment,
    PairingToken,
    S2Role,
    Protocols,
)
from s2python.common import EnergyManagementRole, ControlType, Handshake, ReceptionStatusValues, SelectControlType
from s2python.frbc import (
    FRBCSystemDescription,
)
from s2python.message import S2Message

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("example_s2_server")


def create_signal_handler(server):
    """Create a signal handler function for the given server."""

    def handler(signum, frame):
        logger.info("Received signal %d. Shutting down...", signum)
        server.stop()
        sys.exit(0)

    return handler


async def handle_FRBC_system_description(
    server: S2DefaultWSServer, message: S2Message, send_okay: asyncio.Future
) -> None:
    """Handle FRBC system description messages."""
    if not isinstance(message, FRBCSystemDescription):
        logger.error("Handler for FRBCSystemDescription received a message of the wrong type: %s", type(message))
        return

    logger.info("Received FRBCSystemDescription: %s", message.to_json())
    await server.respond_with_reception_status(
        subject_message_id=message.message_id,
        status=ReceptionStatusValues.OK,
        diagnostic_label="FRBCSystemDescription received",
    )


async def handle_handshake(server: S2DefaultWSServer, message: S2Message, send_okay: asyncio.Future) -> None:
    """Handle handshake messages and send control type selection if client is RM."""
    if not isinstance(message, Handshake):
        logger.error("Handler for Handshake received a message of the wrong type: %s", type(message))
        return

    logger.info("Received Handshake in example_s2_server: %s", message.to_json())

    # Send reception status for the handshake
    await server.respond_with_reception_status(
        subject_message_id=message.message_id,
        status=ReceptionStatusValues.OK,
        diagnostic_label="Handshake received",
    )

    # If client is RM, send control type selection
    if message.role == EnergyManagementRole.RM:
        # First await the send_okay for the handshake
        # await send_okay
        # Then send the control type selection and wait for its reception status
        select_control_type = SelectControlType(
            message_id=uuid.uuid4(),
            control_type=ControlType.FILL_RATE_BASED_CONTROL,
        )
        logger.info("Sending select control type: %s", select_control_type.to_json())
        await server.send_msg_and_await_reception_status_async(select_control_type)


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
        "--instance",
        type=str,
        default="http",
        help="Instance to use (default: http)",
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
    logger.info("http_port: %s", args.http_port)
    logger.info("ws_port: %s", args.ws_port)

    if args.instance == "ws":
        server_ws = S2DefaultWSServer(
            host=args.host,
            port=args.ws_port,
            role=EnergyManagementRole.CEM,
        )
        # Register our custom handshake handler
        server_ws._handlers.register_handler(Handshake, handle_handshake)
        server_ws._handlers.register_handler(FRBCSystemDescription, handle_FRBC_system_description)
        # Create and register signal handlers
        handler = create_signal_handler(server_ws)
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)

        try:
            server_ws.start()
        except KeyboardInterrupt:
            server_ws.stop()
    else:
        server_http = S2DefaultHTTPServer(
            host=args.host,
            http_port=args.http_port,
            ws_port=args.ws_port,
            instance=args.instance,
            server_node_description=server_node_description,
            token=PairingToken(token=args.pairing_token),
            supported_protocols=[Protocols.WebSocketSecure],
        )
        # Create and register signal handlers
        handler = create_signal_handler(server_http)
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)

        try:
            server_http.start_server()
        except KeyboardInterrupt:
            server_http.stop_server()
