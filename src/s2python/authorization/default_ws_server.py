"""
Default implementation of the S2 protocol WebSocket server.
"""

import asyncio
import json
import logging
import threading
import time
import uuid
from typing import Any, Optional, List, Type, Dict, Callable, Awaitable, Union, Tuple
import traceback

import websockets
from websockets.server import WebSocketServerProtocol, serve as ws_serve
from websockets.datastructures import Headers

from s2python.common import (
    ReceptionStatusValues,
    ReceptionStatus,
    Handshake,
    EnergyManagementRole,
    HandshakeResponse,
    SelectControlType,
    ControlType,
)
from s2python.message import S2Message
from s2python.s2_parser import S2Parser
from s2python.s2_validation_error import S2ValidationError
from s2python.communication.reception_status_awaiter import ReceptionStatusAwaiter
from s2python.version import S2_VERSION
from s2python.authorization.database import S2Database

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("S2DefaultWSServer")


class MessageHandlers:
    """Class to manage message handlers for different message types."""

    handlers: Dict[Type[S2Message], Callable]

    def __init__(self) -> None:
        self.handlers = {}

    async def handle_message(
        self,
        server: "S2DefaultWSServer",
        msg: S2Message,
        websocket: WebSocketServerProtocol,
    ) -> None:
        """Handle the S2 message using the registered handler.

        Args:
            server: The server instance handling the message
            msg: The S2 message to handle
            websocket: The websocket connection to the client
        """
        handler = self.handlers.get(type(msg))
        if handler is not None:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(server, msg, websocket)  # type: ignore[arg-type]
                else:

                    def do_message() -> None:
                        handler(server, msg, websocket)  # type: ignore[arg-type]

                    eventloop = asyncio.get_event_loop()
                    await eventloop.run_in_executor(executor=None, func=do_message)
            except Exception:
                logger.error("While processing message %s an unrecoverable error occurred.", msg.message_id)  # type: ignore[attr-defined, union-attr]
                logger.error("Error: %s", traceback.format_exc())
                await server.respond_with_reception_status(
                    subject_message_id=msg.message_id,  # type: ignore[attr-defined, union-attr]
                    status=ReceptionStatusValues.PERMANENT_ERROR,
                    diagnostic_label=f"While processing message {msg.message_id} "  # type: ignore[attr-defined, union-attr]
                    f"an unrecoverable error occurred.",
                    websocket=websocket,
                )
                raise
        else:
            logger.warning(
                "Received a message of type %s but no handler is registered. Ignoring the message.",
                type(msg),
            )

    def register_handler(self, msg_type: Type[S2Message], handler: Callable) -> None:
        """Register a handler for a specific message type.

        Args:
            msg_type: The message type to handle
            handler: The handler function
        """
        self.handlers[msg_type] = handler


class S2DefaultWSServer:
    """Default WebSocket server implementation for S2 protocol."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        role: EnergyManagementRole = EnergyManagementRole.CEM,
        db_path: Optional[str] = None,
    ) -> None:
        """Initialize the WebSocket server.

        Args:
            host: The host to bind to
            port: The port to listen on
            role: The role of this server (CEM or RM)
            db_path: Path to the SQLite database for challenges.
        """
        self.host = host
        self.port = port
        self.role = role
        self._server: Optional[websockets.WebSocketServer] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._eventloop = asyncio.new_event_loop()
        self._handlers = MessageHandlers()
        self.s2_parser = S2Parser()
        self._connections: Dict[str, WebSocketServerProtocol] = {}
        self._stop_event = asyncio.Event()
        self.reception_status_awaiter = ReceptionStatusAwaiter()
        self.reconnect = False
        self.s2_db = S2Database(db_path) if db_path else None
        # Register default handlers
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        """Register default message handlers."""
        self._handlers.register_handler(Handshake, self.handle_handshake)
        self._handlers.register_handler(HandshakeResponse, self.handle_handshake_response)
        self._handlers.register_handler(ReceptionStatus, self.handle_reception_status)

    def start(self) -> None:
        """Start the WebSocket server."""
        self._run_eventloop(self._run_as_cem())

    def _run_eventloop(self, main_task: Awaitable[None]) -> None:
        self._thread = threading.current_thread()
        logger.debug("Starting eventloop for S2DefaultWSServer")
        try:
            self._eventloop.run_until_complete(main_task)
        except asyncio.CancelledError:
            pass
        logger.debug("S2 connection thread has stopped.")

    async def _run_as_cem(self) -> None:
        """Run the S2 connection as a CEM."""
        logger.debug("Connecting as S2 CEM.")

        self._stop_event = asyncio.Event()

        first_run = True

        while (first_run or self.reconnect) and not self._stop_event.is_set():
            first_run = False
            self._restart_connection_event = asyncio.Event()
            await self._connect_and_run()
            time.sleep(1)

        logger.debug("Finished S2 connection eventloop.")

    async def _process_request(
        self, path: str, request_headers: Headers
    ) -> Optional[Tuple[int, List[Tuple[str, str]], bytes]]:
        """
        Process incoming connection requests and validate the challenge.
        """
        if self.s2_db:
            auth_header = request_headers.get("Authorization")
            if not auth_header:
                logger.warning("Connection attempt without Authorization header. Rejecting.")
                return (401, [], b"Unauthorized")

            if not auth_header.startswith("Bearer "):
                logger.warning("Invalid Authorization header format. Rejecting.")
                return (401, [], b"Unauthorized")

            token = auth_header.split(" ", 1)[1]

            if not self.s2_db.verify_and_remove_challenge(token):
                logger.warning("Invalid token provided. Rejecting connection.")
                return (403, [], b"Forbidden")

            logger.info("Token validated. Accepting connection.")

        return None  # Accept connection

    async def _connect_and_run(self) -> None:
        """Connect to the WebSocket server and run the event loop."""
        self._received_messages: asyncio.Queue[S2Message] = asyncio.Queue()
        if self._server is None:
            self._server = await ws_serve(
                self._handle_websocket_connection,
                host=self.host,
                port=self.port,
                process_request=self._process_request,
            )
            logger.info("S2 WebSocket server running at: ws://%s:%s", self.host, self.port)
        else:
            logger.info(
                "S2 WebSocket server already running at: ws://%s:%s",
                self.host,
                self.port,
            )

            async def wait_till_stop() -> None:
                await self._stop_event.wait()

            async def wait_till_connection_restart() -> None:
                await self._restart_connection_event.wait()

            background_tasks = [
                self._eventloop.create_task(wait_till_stop()),
                self._eventloop.create_task(wait_till_connection_restart()),
            ]
            (done, pending) = await asyncio.wait(background_tasks, return_when=asyncio.FIRST_COMPLETED)
        await self._stop_event.wait()

    def stop(self) -> None:
        """Stop the WebSocket server."""
        if self._loop and self._stop_event:
            self._loop.call_soon_threadsafe(self._stop_event.set)
        if self._server:
            self._server.close()

    async def _handle_websocket_connection(self, websocket: WebSocketServerProtocol, path: str) -> None:
        """Handle incoming WebSocket connections.

        Args:
            websocket: The WebSocket connection
            path: The request path
        """
        client_id = str(uuid.uuid4())
        logger.info("Client %s connected on path: %s", client_id, path)
        self._connections[client_id] = websocket

        try:
            async for message in websocket:
                logger.info("message_type: %s", type(message))
                try:
                    s2_msg = self.s2_parser.parse_as_any_message(message)
                    if isinstance(s2_msg, ReceptionStatus):
                        logger.info("Received reception status: %s", s2_msg)
                        await self.reception_status_awaiter.receive_reception_status(s2_msg)
                        continue
                except json.JSONDecodeError:
                    await self.respond_with_reception_status(
                        subject_message_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                        status=ReceptionStatusValues.INVALID_DATA,
                        diagnostic_label="Not valid json.",
                        websocket=websocket,
                    )
                    continue
                try:
                    logger.info("Received message: %s", message)
                    await self._handlers.handle_message(self, s2_msg, websocket)
                except json.JSONDecodeError:
                    await self.respond_with_reception_status(
                        subject_message_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                        status=ReceptionStatusValues.INVALID_DATA,
                        diagnostic_label="Not valid json.",
                        websocket=websocket,
                    )
                except S2ValidationError as e:
                    json_msg = json.loads(message)
                    message_id = json_msg.get("message_id")
                    if message_id:
                        await self.respond_with_reception_status(
                            subject_message_id=message_id,
                            status=ReceptionStatusValues.INVALID_MESSAGE,
                            diagnostic_label=str(e),
                            websocket=websocket,
                        )
                    else:
                        await self.respond_with_reception_status(
                            subject_message_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                            status=ReceptionStatusValues.INVALID_DATA,
                            diagnostic_label="Message appears valid json but could not find a message_id field.",
                            websocket=websocket,
                        )
                except Exception as e:
                    logger.error("Error processing message: %s", str(e))
                    raise

        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection with client %s closed", client_id)
        finally:
            if client_id in self._connections:
                del self._connections[client_id]
            logger.info("Client %s disconnected", client_id)

    async def respond_with_reception_status(
        self,
        subject_message_id: uuid.UUID,
        status: ReceptionStatusValues,
        diagnostic_label: str,
        websocket: WebSocketServerProtocol,
    ) -> None:
        """Send a reception status response.

        Args:
            subject_message_id: The ID of the message being responded to
            status: The reception status
            diagnostic_label: A diagnostic message
            websocket: The websocket connection to send the response to
        """
        response = ReceptionStatus(
            subject_message_id=subject_message_id,
            status=status,
            diagnostic_label=diagnostic_label,
        )
        logger.info("Sending reception status %s for message %s", status, subject_message_id)
        try:
            await websocket.send(response.to_json())
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Connection closed while sending reception status")

    def respond_with_reception_status_sync(
        self,
        subject_message_id: uuid.UUID,
        status: ReceptionStatusValues,
        diagnostic_label: str,
        websocket: WebSocketServerProtocol,
    ) -> None:
        """Synchronous version of respond_with_reception_status."""
        if self._loop:
            asyncio.run_coroutine_threadsafe(
                self.respond_with_reception_status(subject_message_id, status, diagnostic_label, websocket),
                self._loop,
            ).result()

    async def send_msg_and_await_reception_status_async(
        self,
        s2_msg: S2Message,
        websocket: WebSocketServerProtocol,
        timeout_reception_status: float = 20.0,
        raise_on_error: bool = True,
    ) -> ReceptionStatus:
        """Send a message and await a reception status.

        Args:
            s2_msg: The message to send
            websocket: The websocket connection to send the message to
            timeout_reception_status: The timeout for the reception status
            raise_on_error: Whether to raise an error if the reception status is not received
        """
        await self._send_and_forget(s2_msg, websocket)
        logger.debug(
            "Waiting for ReceptionStatus for %s %s for %s seconds",
            s2_msg.message_type,
            s2_msg.message_id,  # type: ignore[attr-defined, union-attr]
            timeout_reception_status,
        )
        try:
            try:
                response = await websocket.recv()
                logger.info("Received reception status: %s", response)
                reception_status = ReceptionStatus(
                    subject_message_id=s2_msg.message_id,  # type: ignore[attr-defined, union-attr]
                    status=ReceptionStatusValues.OK,
                    diagnostic_label="Reception status received.",
                )
                return reception_status
            except websockets.exceptions.ConnectionClosedOK:
                logger.warning("Connection closed while waiting for reception status")
                return ReceptionStatus(
                    subject_message_id=s2_msg.message_id,  # type: ignore[attr-defined, union-attr]
                    status=ReceptionStatusValues.OK,
                    diagnostic_label="Connection closed, assuming OK status.",
                )
        except TimeoutError:
            if raise_on_error:
                raise
            logger.error(
                "Did not receive a reception status on time for %s %s",
                s2_msg.message_type,
                s2_msg.message_id,  # type: ignore[attr-defined, union-attr]
            )
            return ReceptionStatus(
                subject_message_id=s2_msg.message_id,  # type: ignore[attr-defined, union-attr]
                status=ReceptionStatusValues.PERMANENT_ERROR,
                diagnostic_label="Timeout waiting for reception status.",
            )

    async def handle_handshake(
        self,
        _: "S2DefaultWSServer",
        message: S2Message,
        websocket: WebSocketServerProtocol,
    ) -> None:
        """Handle handshake messages.

        Args:
            _: The server instance
            message: The handshake message
            websocket: The websocket connection to the client
        """
        if not isinstance(message, Handshake):
            logger.error(
                "Handler for Handshake received a message of the wrong type: %s",
                type(message),
            )
            return

        logger.info("Received Handshak(In WS Server): %s", message.to_json())
        handshake_response = HandshakeResponse(
            message_id=message.message_id,
            selected_protocol_version=message.supported_protocol_versions,
        )
        await self.send_msg_and_await_reception_status_async(handshake_response, websocket)

        await self.respond_with_reception_status(
            subject_message_id=message.message_id,
            status=ReceptionStatusValues.OK,
            diagnostic_label="Handshake received",
            websocket=websocket,
        )
        logger.debug(
            "%s supports S2 protocol versions: %s",
            message.role,
            message.supported_protocol_versions,
        )

    async def handle_reception_status(
        self,
        _: "S2DefaultWSServer",
        message: S2Message,
        websocket: WebSocketServerProtocol,
    ) -> None:
        """Handle reception status messages."""
        if not isinstance(message, ReceptionStatus):
            logger.error(
                "Handler for ReceptionStatus received a message of the wrong type: %s",
                type(message),
            )
            return
        logger.info("Received ReceptionStatus in handle_reception_status: %s", message.to_json())

    async def handle_handshake_response(
        self,
        _: "S2DefaultWSServer",
        message: S2Message,
        websocket: WebSocketServerProtocol,
    ) -> None:
        """Handle handshake response messages.

        Args:
            _: The server instance
            message: The handshake response message
            websocket: The websocket connection to the client
        """
        if not isinstance(message, HandshakeResponse):
            logger.error(
                "Handler for HandshakeResponse received a message of the wrong type: %s",
                type(message),
            )
            return

        logger.debug("Received HandshakeResponse: %s", message.to_json())

    async def _send_and_forget(self, s2_msg: S2Message, websocket: WebSocketServerProtocol) -> None:
        """Send a message and forget about it.

        Args:
            s2_msg: The message to send
            websocket: The websocket connection to send the message to
        """
        try:
            await websocket.send(s2_msg.to_json())
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Connection closed while sending message")

    async def send_select_control_type(
        self,
        control_type: ControlType,
        websocket: WebSocketServerProtocol,
        send_okay: Awaitable[None],
    ) -> None:
        """Select the control type.

        Args:
            control_type: The control type to select
            websocket: The websocket connection to send the message to
            send_okay: Coroutine to send OK status
        """
        logger.info("Selecting control type %s", control_type)
        select_control_type = SelectControlType(
            message_id=uuid.uuid4(),
            control_type=control_type,
        )
        await self._send_and_forget(select_control_type, websocket)
        await send_okay
