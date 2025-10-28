from s2python.common import ReceptionStatus
from s2python.message import S2MessageWithID


class S2Connection:  # pylint: disable=too-many-instance-attributes
    url: str
    reconnect: bool
    reception_status_awaiter: ReceptionStatusAwaiter
    ws: Optional[WSConnection]
    s2_parser: S2Parser
    control_types: List[S2ControlType]
    role: EnergyManagementRole
    asset_details: AssetDetails

    _thread: threading.Thread

    _handlers: MessageHandlers
    _current_control_type: Optional[S2ControlType]
    _received_messages: asyncio.Queue

    _eventloop: asyncio.AbstractEventLoop
    _stop_event: asyncio.Event
    _restart_connection_event: asyncio.Event
    _verify_certificate: bool
    _bearer_token: Optional[str]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        url: str,
        role: EnergyManagementRole,
        control_types: List[S2ControlType],
        asset_details: AssetDetails,
        reconnect: bool = False,
        verify_certificate: bool = True,
        bearer_token: Optional[str] = None,
    ) -> None:
        self.url = url
        self.reconnect = reconnect
        self.reception_status_awaiter = ReceptionStatusAwaiter()
        self.ws = None
        self.s2_parser = S2Parser()

        self._handlers = MessageHandlers()
        self._current_control_type = None

        self._eventloop = asyncio.new_event_loop()

        self.control_types = control_types
        self.role = role
        self.asset_details = asset_details
        self._verify_certificate = verify_certificate

        self._handlers.register_handler(
            SelectControlType, self._handle_select_control_type_as_rm
        )
        self._handlers.register_handler(Handshake, self._handle_handshake)
        self._handlers.register_handler(HandshakeResponse, self._handle_handshake_response_as_rm)
        self._bearer_token = bearer_token

    def start_as_rm(self) -> None:
        self._run_eventloop(self._run_as_rm())

    def _run_eventloop(self, main_task: Awaitable[None]) -> None:
        self._thread = threading.current_thread()
        logger.debug("Starting eventloop")
        try:
            self._eventloop.run_until_complete(main_task)
        except asyncio.CancelledError:
            pass
        logger.debug("S2 connection thread has stopped.")

    def stop(self) -> None:
        """Stops the S2 connection.

        Note: Ensure this method is called from a different thread than the thread running the S2 connection.
        Otherwise it will block waiting on the coroutine _do_stop to terminate successfully but it can't run
        the coroutine. A `RuntimeError` will be raised to prevent the indefinite block.
        """
        if threading.current_thread() == self._thread:
            raise RuntimeError(
                "Do not call stop from the thread running the S2 connection. This results in an infinite block!"
            )
        if self._eventloop.is_running():
            asyncio.run_coroutine_threadsafe(self._do_stop(), self._eventloop).result()
        self._thread.join()
        logger.info("Stopped the S2 connection.")

    async def _do_stop(self) -> None:
        logger.info("Will stop the S2 connection.")
        self._stop_event.set()

    async def _run_as_rm(self) -> None:
        logger.debug("Connecting as S2 resource manager.")

        self._stop_event = asyncio.Event()

        first_run = True

        while (first_run or self.reconnect) and not self._stop_event.is_set():
            first_run = False
            self._restart_connection_event = asyncio.Event()
            await self._connect_and_run()
            time.sleep(1)

        logger.debug("Finished S2 connection eventloop.")

    async def _connect_and_run(self) -> None:
        self._received_messages = asyncio.Queue()
        await self._connect_ws()
        if self.ws:

            async def wait_till_stop() -> None:
                await self._stop_event.wait()

            async def wait_till_connection_restart() -> None:
                await self._restart_connection_event.wait()

            background_tasks = [
                self._eventloop.create_task(self._receive_messages()),
                self._eventloop.create_task(wait_till_stop()),
                self._eventloop.create_task(self._connect_as_rm()),
                self._eventloop.create_task(wait_till_connection_restart()),
            ]

            (done, pending) = await asyncio.wait(
                background_tasks, return_when=asyncio.FIRST_COMPLETED
            )
            if self._current_control_type:
                self._current_control_type.deactivate(self)
                self._current_control_type = None

            for task in done:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                except (
                    websockets.ConnectionClosedError,
                    websockets.ConnectionClosedOK,
                ):
                    logger.info("The other party closed the websocket connection.")

            for task in pending:
                try:
                    task.cancel()
                    await task
                except asyncio.CancelledError:
                    pass

            await self.ws.close()
            await self.ws.wait_closed()

    async def _connect_ws(self) -> None:
        try:
            # set up connection arguments for SSL and bearer token, if required
            connection_kwargs: Dict[str, Any] = {}
            if self.url.startswith("wss://") and not self._verify_certificate:
                connection_kwargs["ssl"] = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                connection_kwargs["ssl"].check_hostname = False
                connection_kwargs["ssl"].verify_mode = ssl.CERT_NONE

            if self._bearer_token:
                connection_kwargs["additional_headers"] = {
                    "Authorization": f"Bearer {self._bearer_token}"
                }

            self.ws = await ws_connect(uri=self.url, **connection_kwargs)
        except (EOFError, OSError) as e:
            logger.info("Could not connect due to: %s", str(e))

    async def _connect_as_rm(self) -> None:
        await self._send_msg_and_await_reception_status_async(
            Handshake(
                message_id=uuid.uuid4(),
                role=self.role,
                supported_protocol_versions=[S2_VERSION],
            )
        )
        logger.debug(
            "Send handshake to CEM. Expecting Handshake and HandshakeResponse from CEM."
        )

        await self._handle_received_messages()

    async def _handle_handshake(
        self, _: "S2Connection", message: S2Message, send_okay: Awaitable[None]
    ) -> None:
        if not isinstance(message, Handshake):
            logger.error(
                "Handler for Handshake received a message of the wrong type: %s",
                type(message),
            )
            return

        logger.debug(
            "%s supports S2 protocol versions: %s",
            message.role,
            message.supported_protocol_versions,
        )
        await send_okay

    async def _handle_handshake_response_as_rm(
        self, _: "S2Connection", message: S2Message, send_okay: Awaitable[None]
    ) -> None:
        if not isinstance(message, HandshakeResponse):
            logger.error(
                "Handler for HandshakeResponse received a message of the wrong type: %s",
                type(message),
            )
            return

        logger.debug("Received HandshakeResponse %s", message.to_json())

        logger.debug(
            "CEM selected to use version %s", message.selected_protocol_version
        )
        await send_okay
        logger.debug("Handshake complete. Sending first ResourceManagerDetails.")

        await self._send_msg_and_await_reception_status_async(
            self.asset_details.to_resource_manager_details(self.control_types)
        )

    async def _handle_select_control_type_as_rm(
        self, _: "S2Connection", message: S2Message, send_okay: Awaitable[None]
    ) -> None:
        if not isinstance(message, SelectControlType):
            logger.error(
                "Handler for SelectControlType received a message of the wrong type: %s",
                type(message),
            )
            return

        await send_okay

        logger.debug(
            "CEM selected control type %s. Activating control type.",
            message.control_type,
        )

        control_types_by_protocol_name = {
            c.get_protocol_control_type(): c for c in self.control_types
        }
        selected_control_type: Optional[S2ControlType] = (
            control_types_by_protocol_name.get(message.control_type)
        )

        if self._current_control_type is not None:
            await self._eventloop.run_in_executor(
                None, self._current_control_type.deactivate, self
            )

        self._current_control_type = selected_control_type

        if self._current_control_type is not None:
            await self._eventloop.run_in_executor(
                None, self._current_control_type.activate, self
            )
            self._current_control_type.register_handlers(self._handlers)

    async def _receive_messages(self) -> None:
        """Receives all incoming messages in the form of a generator.

        Will also receive the ReceptionStatus messages but instead of yielding these messages, they are routed
        to any calls of `send_msg_and_await_reception_status`.
        """
        if self.ws is None:
            raise RuntimeError(
                "Cannot receive messages if websocket connection is not yet established."
            )

        logger.info("S2 connection has started to receive messages.")

        async for message in self.ws:
            try:
                s2_msg: S2Message = self.s2_parser.parse_as_any_message(message)
            except json.JSONDecodeError:
                await self._send_and_forget(
                    ReceptionStatus(
                        subject_message_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                        status=ReceptionStatusValues.INVALID_DATA,
                        diagnostic_label="Not valid json.",
                    )
                )
            except S2ValidationError as e:
                json_msg = json.loads(message)
                message_id = json_msg.get("message_id")
                if message_id:
                    await self._respond_with_reception_status(
                        subject_message_id=message_id,
                        status=ReceptionStatusValues.INVALID_MESSAGE,
                        diagnostic_label=str(e),
                    )
                else:
                    await self._respond_with_reception_status(
                        subject_message_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                        status=ReceptionStatusValues.INVALID_DATA,
                        diagnostic_label="Message appears valid json but could not find a message_id field.",
                    )
            else:
                logger.debug("Received message %s", s2_msg.to_json())

                if isinstance(s2_msg, ReceptionStatus):
                    logger.debug(
                        "Message is a reception status for %s so registering in cache.",
                        s2_msg.subject_message_id,
                    )
                    await self.reception_status_awaiter.receive_reception_status(s2_msg)
                else:
                    await self._received_messages.put(s2_msg)

    async def _send_and_forget(self, s2_msg: S2Message) -> None:
        if self.ws is None:
            raise RuntimeError(
                "Cannot send messages if websocket connection is not yet established."
            )

        json_msg = s2_msg.to_json()
        logger.debug("Sending message %s", json_msg)
        try:
            await self.ws.send(json_msg)
        except websockets.ConnectionClosedError as e:
            logger.error("Unable to send message %s due to %s", s2_msg, str(e))
            self._restart_connection_event.set()

    async def _respond_with_reception_status(
        self, subject_message_id: uuid.UUID, status: ReceptionStatusValues, diagnostic_label: str
    ) -> None:
        logger.debug(
            "Responding to message %s with status %s", subject_message_id, status
        )
        await self._send_and_forget(
            ReceptionStatus(
                subject_message_id=subject_message_id,
                status=status,
                diagnostic_label=diagnostic_label,
            )
        )

    def respond_with_reception_status_sync(
        self, subject_message_id: uuid.UUID, status: ReceptionStatusValues, diagnostic_label: str
    ) -> None:
        asyncio.run_coroutine_threadsafe(
            self._respond_with_reception_status(
                subject_message_id, status, diagnostic_label
            ),
            self._eventloop,
        ).result()

    async def _send_msg_and_await_reception_status_async(
        self,
        s2_msg: S2MessageWithID,
        timeout_reception_status: float = 5.0,
        raise_on_error: bool = True,
    ) -> ReceptionStatus:
        await self._send_and_forget(s2_msg)
        logger.debug(
            "Waiting for ReceptionStatus for %s %s seconds",
            s2_msg.message_id,  # type: ignore[attr-defined, union-attr]
            timeout_reception_status,
        )
        try:
            reception_status = await self.reception_status_awaiter.wait_for_reception_status(
                s2_msg.message_id, timeout_reception_status  # type: ignore[attr-defined, union-attr]
            )
        except TimeoutError:
            logger.error(
                "Did not receive a reception status on time for %s",
                s2_msg.message_id,  # type: ignore[attr-defined, union-attr]
            )
            self._stop_event.set()
            raise

        if reception_status.status != ReceptionStatusValues.OK and raise_on_error:
            raise RuntimeError(
                f"ReceptionStatus was not OK but rather {reception_status.status}"
            )

        return reception_status

    def send_msg_and_await_reception_status_sync(
        self,
        s2_msg: S2MessageWithID,
        timeout_reception_status: float = 5.0,
        raise_on_error: bool = True,
    ) -> ReceptionStatus:
        return asyncio.run_coroutine_threadsafe(
            self._send_msg_and_await_reception_status_async(
                s2_msg, timeout_reception_status, raise_on_error
            ),
            self._eventloop,
        ).result()

    async def _handle_received_messages(self) -> None:
        while True:
            msg = await self._received_messages.get()
            await self._handlers.handle_message(self, msg)