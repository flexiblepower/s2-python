"""
Example S2 server implementation using Flask.

This example demonstrates how to set up both an HTTP and a WebSocket server
using the Flask-based implementations.

Note: You need to install Flask and Flask-Sock:
  `pip install flask flask-sock`

For running the WebSocket server with true async capabilities, an ASGI server
like Hypercorn is recommended:
  `pip install hypercorn`
  `hypercorn examples.example_flask_server:server_ws.app`
"""

import argparse
import logging
import signal
import sys
import uuid

from flask_sock import Sock

from s2python.authorization.flask_http_server import S2FlaskHTTPServer
from s2python.authorization.flask_ws_server import S2FlaskWSServer
from s2python.common import (
    ControlType,
    EnergyManagementRole,
    Handshake,
    HandshakeResponse,
    ReceptionStatusValues,
    ResourceManagerDetails,
    SelectControlType,
)
from s2python.frbc import (
    FRBCActuatorStatus,
    FRBCFillLevelTargetProfile,
    FRBCStorageStatus,
    FRBCSystemDescription,
)
from s2python.generated.gen_s2_pairing import (
    Deployment,
    PairingToken,
    Protocols,
    S2NodeDescription,
    S2Role,
)
from s2python.message import S2Message

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("example_flask_server")

# Create the server instance at the module level so Hypercorn can find it.
# We assume 'ws' mode for ASGI server execution.
server_instance = S2FlaskWSServer(
    host="localhost",  # These values can be configured via env vars or other means
    port=8080,
    role=EnergyManagementRole.CEM,
)


def create_signal_handler():
    """Create a signal handler function."""

    def handler(signum, frame):
        logger.info("Received signal %d. Shutting down...", signum)
        if server_instance:
            server_instance.stop()
        # For Flask's dev server, this will be interrupted by the signal.
        # For production servers (gunicorn, hypercorn), they handle signals for shutdown.
        sys.exit(0)

    return handler


async def handle_FRBC_system_description(server: S2FlaskWSServer, message: S2Message, websocket: Sock) -> None:
    """Handle FRBC system description messages."""
    if not isinstance(message, FRBCSystemDescription):
        logger.error(
            "Handler for FRBCSystemDescription received a message of the wrong type: %s",
            type(message),
        )
        return

    logger.info("Received FRBCSystemDescription: %s", message.to_json())
    await server.respond_with_reception_status(
        subject_message_id=message.message_id,
        status=ReceptionStatusValues.OK,
        diagnostic_label="FRBCSystemDescription received",
        websocket=websocket,
    )


async def handle_FRBCActuatorStatus(server: S2FlaskWSServer, message: S2Message, websocket: Sock) -> None:
    """Handle FRBCActuatorStatus messages."""
    if not isinstance(message, FRBCActuatorStatus):
        logger.error(
            "Handler for FRBCActuatorStatus received a message of the wrong type: %s",
            type(message),
        )
        return

    logger.info("Received FRBCActuatorStatus: %s", message.to_json())
    await server.respond_with_reception_status(
        subject_message_id=message.message_id,
        status=ReceptionStatusValues.OK,
        diagnostic_label="FRBCActuatorStatus received",
        websocket=websocket,
    )


async def handle_FillLevelTargetProfile(server: S2FlaskWSServer, message: S2Message, websocket: Sock) -> None:
    """Handle FillLevelTargetProfile messages."""
    if not isinstance(message, FRBCFillLevelTargetProfile):
        logger.error(
            "Handler for FillLevelTargetProfile received a message of the wrong type: %s",
            type(message),
        )
        return

    logger.info("Received FillLevelTargetProfile: %s", message.to_json())
    await server.respond_with_reception_status(
        subject_message_id=message.message_id,
        status=ReceptionStatusValues.OK,
        diagnostic_label="FillLevelTargetProfile received",
        websocket=websocket,
    )


async def handle_FRBCStorageStatus(server: S2FlaskWSServer, message: S2Message, websocket: Sock) -> None:
    """Handle FRBCStorageStatus messages."""
    if not isinstance(message, FRBCStorageStatus):
        logger.error(
            "Handler for FRBCStorageStatus received a message of the wrong type: %s",
            type(message),
        )
        return

    logger.info("Received FRBCStorageStatus: %s", message.to_json())
    await server.respond_with_reception_status(
        subject_message_id=message.message_id,
        status=ReceptionStatusValues.OK,
        diagnostic_label="FRBCStorageStatus received",
        websocket=websocket,
    )


async def handle_ResourceManagerDetails(server: S2FlaskWSServer, message: S2Message, websocket: Sock) -> None:
    """Handle ResourceManagerDetails messages."""
    if not isinstance(message, ResourceManagerDetails):
        logger.error(
            "Handler for ResourceManagerDetails received a message of the wrong type: %s",
            type(message),
        )
        return

    logger.info("Received ResourceManagerDetails: %s", message.to_json())
    await server.respond_with_reception_status(
        subject_message_id=message.message_id,
        status=ReceptionStatusValues.OK,
        diagnostic_label="ResourceManagerDetails received",
        websocket=websocket,
    )


async def handle_handshake(server: S2FlaskWSServer, message: S2Message, websocket: Sock) -> None:
    """Handle handshake messages and send control type selection if client is RM."""
    if not isinstance(message, Handshake):
        logger.error(
            "Handler for Handshake received a message of the wrong type: %s",
            type(message),
        )
        return

    logger.info("Received Handshake in example_flask_server: %s", message.to_json())

    # Send reception status for the handshake
    await server.respond_with_reception_status(
        subject_message_id=message.message_id,
        status=ReceptionStatusValues.OK,
        diagnostic_label="Handshake received",
        websocket=websocket,
    )

    handshake_response = HandshakeResponse(
        message_id=message.message_id,
        selected_protocol_version="1.0",
    )
    logger.info("Sent HandshakeResponse: %s", handshake_response.to_json())
    await server._send_and_forget(handshake_response, websocket)

    # If client is RM, send control type selection
    if message.role == EnergyManagementRole.RM:
        select_control_type = SelectControlType(
            message_id=uuid.uuid4(),
            control_type=ControlType.FILL_RATE_BASED_CONTROL,
        )
        logger.info("Sending select control type: %s", select_control_type.to_json())
        await server.send_msg_and_await_reception_status_async(select_control_type, websocket)

# Register handlers on the globally defined instance
server_instance._handlers.register_handler(Handshake, handle_handshake)
server_instance._handlers.register_handler(FRBCSystemDescription, handle_FRBC_system_description)
server_instance._handlers.register_handler(ResourceManagerDetails, handle_ResourceManagerDetails)
server_instance._handlers.register_handler(FRBCActuatorStatus, handle_FRBCActuatorStatus)
server_instance._handlers.register_handler(FRBCFillLevelTargetProfile, handle_FillLevelTargetProfile)
server_instance._handlers.register_handler(FRBCStorageStatus, handle_FRBCStorageStatus)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example S2 server implementation using Flask.")
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
        choices=["http", "ws"],
        help="Instance to use (http or ws, default: http)",
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
        modelName="S2 server example (Flask)",
        userDefinedName="TNO S2 server example for frbc using Flask",
        role=S2Role.RM,
        deployment=Deployment.LAN,
    )
    logger.info("http_port: %s", args.http_port)
    logger.info("ws_port: %s", args.ws_port)

    # Setup signal handling
    handler = create_signal_handler()
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    if args.instance == "ws":
        logger.info(
            "Starting Flask WebSocket server. For async, run with 'hypercorn examples.example_flask_server:server_ws.app'"
        )
        try:
            server_instance.start()
        except KeyboardInterrupt:
            handler(signal.SIGINT, None)
    else:
        server_http = S2FlaskHTTPServer(
            host=args.host,
            http_port=args.http_port,
            ws_port=args.ws_port,
            instance=args.instance,
            server_node_description=server_node_description,
            token=PairingToken(token=args.pairing_token),
            supported_protocols=[Protocols.WebSocketSecure],
        )
        server_instance = server_http  # type: ignore[assignment]

        logger.info("Starting Flask HTTP server.")
        try:
            # Note: server_http.start_server() uses Flask's development server.
            server_http.start_server()
        except KeyboardInterrupt:
            handler(signal.SIGINT, None)
