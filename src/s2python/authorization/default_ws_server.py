"""
Default implementation of the S2 protocol WebSocket server.
"""

import asyncio
import json
import logging
import threading
import time
import uuid
from typing import Any, Optional, List, Type, Dict, Callable, Awaitable, Union
import traceback

import websockets
from websockets.server import WebSocketServerProtocol, serve as ws_serve

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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("S2DefaultWSServer")


class SendOkay:
    """Helper class to manage sending reception status."""

    status_is_send: threading.Event
    server: "S2DefaultWSServer"
    subject_message_id: uuid.UUID

    def __init__(self, server: "S2DefaultWSServer", subject_message_id: uuid.UUID):
        self.status_is_send = threading.Event()
        self.server = server
        self.subject_message_id = subject_message_id

    async def run_async(self) -> None:
        """Send OK reception status asynchronously."""
        self.status_is_send.set()
        await self.server.respond_with_reception_status(
            subject_message_id=self.subject_message_id,
            status=ReceptionStatusValues.OK,
            diagnostic_label="Processed okay.",
        )

    def run_sync(self) -> None:
        """Send OK reception status synchronously."""
        self.status_is_send.set()
        self.server.respond_with_reception_status_sync(
            subject_message_id=self.subject_message_id,
            status=ReceptionStatusValues.OK,
            diagnostic_label="Processed okay.",
        )

    async def ensure_send_async(self, type_msg: Type[S2Message]) -> None:
        """Ensure reception status is sent asynchronously."""
        if not self.status_is_send.is_set():
            logger.warning(
                "Handler for message %s %s did not call send_okay / function to send the ReceptionStatus. "
                "Sending it now.",
                type_msg,
                self.subject_message_id,
            )
            await self.run_async()

    def ensure_send_sync(self, type_msg: Type[S2Message]) -> None:
        """Ensure reception status is sent synchronously."""
        if not self.status_is_send.is_set():
            logger.warning(
                "Handler for message %s %s did not call send_okay / function to send the ReceptionStatus. "
                "Sending it now.",
                type_msg,
                self.subject_message_id,
            )
            self.run_sync()


class MessageHandlers:
    """Class to manage message handlers for different message types."""

    handlers: Dict[Type[S2Message], Callable]

    def __init__(self) -> None:
        self.handlers = {}

    async def handle_message(self, server: "S2DefaultWSServer", msg: S2Message) -> None:
        """Handle the S2 message using the registered handler.

        Args:
            server: The server instance handling the message
            msg: The S2 message to handle
        """
        handler = self.handlers.get(type(msg))
        if handler is not None:
            send_okay = SendOkay(server, msg.message_id)  # type: ignore[attr-defined, union-attr]

            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(server, msg, send_okay.run_async())  # type: ignore[arg-type]
                    await send_okay.ensure_send_async(type(msg))
                else:

                    def do_message() -> None:
                        handler(server, msg, send_okay.run_sync)  # type: ignore[arg-type]
                        send_okay.ensure_send_sync(type(msg))

                    eventloop = asyncio.get_event_loop()
                    await eventloop.run_in_executor(executor=None, func=do_message)
            except Exception:
                if not send_okay.status_is_send.is_set():
                    logger.error("While processing message %s an unrecoverable error occurred.", msg.message_id)  # type: ignore[attr-defined, union-attr]
                    logger.error("Error: %s", traceback.format_exc())
                    await server.respond_with_reception_status(
                        subject_message_id=msg.message_id,  # type: ignore[attr-defined, union-attr]
                        status=ReceptionStatusValues.PERMANENT_ERROR,
                        diagnostic_label=f"While processing message {msg.message_id} "  # type: ignore[attr-defined, union-attr]
                        f"an unrecoverable error occurred.",
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
    ) -> None:
        """Initialize the WebSocket server.

        Args:
            host: The host to bind to
            port: The port to listen on
            role: The role of this server (CEM or RM)
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
        self._received_messages = asyncio.Queue()
        # Register default handlers
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        """Register default message handlers."""
        self._handlers.register_handler(Handshake, self.handle_handshake)
        self._handlers.register_handler(HandshakeResponse, self.handle_handshake_response)

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

    async def _connect_and_run(self) -> None:
        """Connect to the WebSocket server and run the event loop."""
        self._received_messages = asyncio.Queue()
        if self._server is None:
            self._server = await ws_serve(
                self._handle_websocket_connection,
                host=self.host,
                port=self.port,
                process_request=self._handlers.handle_message,
            )
            logger.info("S2 WebSocket server running at: ws://%s:%s", self.host, self.port)
        else:
            logger.info("S2 WebSocket server already running at: ws://%s:%s", self.host, self.port)

            async def wait_till_stop() -> None:
                await self._stop_event.wait()

            async def wait_till_connection_restart() -> None:
                await self._restart_connection_event.wait()

            background_tasks = [
                self._eventloop.create_task(self.receive_messages()),
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
                if isinstance(message, ReceptionStatus):
                    logger.info("--------------->  Received reception status: %s", message)
                    await self.reception_status_awaiter.receive_reception_status(message)
                    continue
                try:
                    logger.info("--------------->  Received message: %s", message)
                    # Parse the message
                    s2_msg = self.s2_parser.parse_as_any_message(message)
                    # Handle the message
                    await self._handlers.handle_message(self, s2_msg)
                except json.JSONDecodeError:
                    await self.respond_with_reception_status(
                        subject_message_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                        status=ReceptionStatusValues.INVALID_DATA,
                        diagnostic_label="Not valid json.",
                    )
                except S2ValidationError as e:
                    json_msg = json.loads(message)
                    message_id = json_msg.get("message_id")
                    if message_id:
                        await self.respond_with_reception_status(
                            subject_message_id=message_id,
                            status=ReceptionStatusValues.INVALID_MESSAGE,
                            diagnostic_label=str(e),
                        )
                    else:
                        await self.respond_with_reception_status(
                            subject_message_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                            status=ReceptionStatusValues.INVALID_DATA,
                            diagnostic_label="Message appears valid json but could not find a message_id field.",
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
    ) -> None:
        """Send a reception status response.

        Args:
            subject_message_id: The ID of the message being responded to
            status: The reception status
            diagnostic_label: A diagnostic message
        """
        response = ReceptionStatus(
            subject_message_id=subject_message_id,
            status=status,
            diagnostic_label=diagnostic_label,
        )
        logger.info("Sending reception status %s for message %s", status, subject_message_id)
        # Send to all connected clients
        for websocket in self._connections.values():
            try:
                await websocket.send(response.to_json())
                logger.info("SENT RECEPTION STATUS-----")
            except websockets.exceptions.ConnectionClosed:
                continue
        logger.info("SENT RECEPTION STATUS-----DONE")

    def respond_with_reception_status_sync(
        self,
        subject_message_id: uuid.UUID,
        status: ReceptionStatusValues,
        diagnostic_label: str,
    ) -> None:
        """Synchronous version of respond_with_reception_status."""
        if self._loop:
            asyncio.run_coroutine_threadsafe(
                self.respond_with_reception_status(subject_message_id, status, diagnostic_label),
                self._loop,
            ).result()

    async def send_msg_and_await_reception_status_async(
        self,
        s2_msg: S2Message,
        timeout_reception_status: float = 20.0,
        raise_on_error: bool = True,
    ) -> ReceptionStatus:
        await self._send_and_forget(s2_msg)
        logger.debug(
            "Waiting for ReceptionStatus for %s %s seconds",
            s2_msg.message_id,  # type: ignore[attr-defined, union-attr]
            timeout_reception_status,
        )
        try:
            logger.info("Waiting for reception status for %s", s2_msg.message_id)
            reception_status = await self.reception_status_awaiter.wait_for_reception_status(
                s2_msg.message_id, timeout_reception_status  # type: ignore[attr-defined, union-attr]
            )
        except TimeoutError:
            if raise_on_error:
                raise
            logger.error(
                "Did not receive a reception status on time for %s",
                s2_msg.message_id,  # type: ignore[attr-defined, union-attr]
            )
            return ReceptionStatus(
                subject_message_id=s2_msg.message_id,  # type: ignore[attr-defined, union-attr]
                status=ReceptionStatusValues.PERMANENT_ERROR,
                diagnostic_label="Timeout waiting for reception status.",
            )
        return reception_status

    async def handle_handshake(self, _: "S2DefaultWSServer", message: S2Message, send_okay: Awaitable[None]) -> None:
        """Handle handshake messages.

        Args:
            _: The server instance
            message: The handshake message
            send_okay: Coroutine to send OK status
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
        await self.send_msg_and_await_reception_status_async(handshake_response)

        await self.respond_with_reception_status(
            subject_message_id=message.message_id,
            status=ReceptionStatusValues.OK,
            diagnostic_label="Handshake received",
        )
        logger.debug(
            "%s supports S2 protocol versions: %s",
            message.role,
            message.supported_protocol_versions,
        )
        await send_okay

    async def handle_handshake_response(
        self, _: "S2DefaultWSServer", message: S2Message, send_okay: Awaitable[None]
    ) -> None:
        """Handle handshake response messages.

        Args:
            _: The server instance
            message: The handshake response message
            send_okay: Coroutine to send OK status
        """
        if not isinstance(message, HandshakeResponse):
            logger.error(
                "Handler for HandshakeResponse received a message of the wrong type: %s",
                type(message),
            )
            return

        logger.debug("Received HandshakeResponse: %s", message.to_json())
        await send_okay

    async def _send_and_forget(self, s2_msg: S2Message) -> None:
        """Send a message and forget about it."""
        for websocket in self._connections.values():
            try:
                await websocket.send(s2_msg.to_json())
            except websockets.exceptions.ConnectionClosed:
                continue

    async def send_select_control_type(self, control_type: ControlType, send_okay: Awaitable[None]) -> None:
        """Select the control type."""
        logger.info("Selecting control type %s", control_type)
        select_control_type = SelectControlType(
            message_id=uuid.uuid4(),
            control_type=control_type,
        )
        await self.send_msg_and_await_reception_status_async(select_control_type)
        # await send_okay

    async def receive_messages(self) -> None:
        """Receive messages from all connected WebSocket clients.

        This method continuously processes messages from all connected clients
        and handles them according to the registered message handlers.
        """
        logger.info("S2 server has started to receive messages.")

        while not self._stop_event.is_set():
            try:
                # Process messages from all connected clients
                for client_id, websocket in list(self._connections.items()):
                    try:
                        async for message in websocket:
                            if isinstance(message, ReceptionStatus):
                                await self.reception_status_awaiter.receive_reception_status(message)
                                continue

                            try:
                                s2_msg: S2Message = self.s2_parser.parse_as_any_message(message)
                                logger.debug("Received message %s", s2_msg.to_json())

                                if isinstance(s2_msg, ReceptionStatus):
                                    logger.debug(
                                        "Message is a reception status for %s so registering in cache.",
                                        s2_msg.subject_message_id,
                                    )
                                    await self.reception_status_awaiter.receive_reception_status(s2_msg)
                                else:
                                    await self._received_messages.put(s2_msg)
                            except json.JSONDecodeError:
                                await self.respond_with_reception_status(
                                    subject_message_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                                    status=ReceptionStatusValues.INVALID_DATA,
                                    diagnostic_label="Not valid json.",
                                )
                            except S2ValidationError as e:
                                json_msg = json.loads(message)
                                message_id = json_msg.get("message_id")
                                if message_id:
                                    await self.respond_with_reception_status(
                                        subject_message_id=message_id,
                                        status=ReceptionStatusValues.INVALID_MESSAGE,
                                        diagnostic_label=str(e),
                                    )
                                else:
                                    await self.respond_with_reception_status(
                                        subject_message_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                                        status=ReceptionStatusValues.INVALID_DATA,
                                        diagnostic_label="Message appears valid json but could not find a message_id field.",
                                    )
                    except websockets.exceptions.ConnectionClosed:
                        logger.info("Connection with client %s closed", client_id)
                        if client_id in self._connections:
                            del self._connections[client_id]
                        continue

                # Process received messages
                while not self._received_messages.empty():
                    msg = await self._received_messages.get()
                    logger.info("Processing message in receive_messages %s", msg.to_json())
                    await self._handlers.handle_message(self, msg)

                # Small delay to prevent busy waiting
                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error("Error in receive_messages: %s", str(e))
                logger.error(traceback.format_exc())
                if not self._stop_event.is_set():
                    await asyncio.sleep(1)  # Wait before retrying
