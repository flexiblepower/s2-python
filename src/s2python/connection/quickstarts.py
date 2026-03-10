import asyncio
import logging
import threading

from s2python.connection.asset_details import AssetDetails
from s2python.connection.async_ import WebsocketClientMedium
from s2python.connection.sync import S2SyncConnection
from s2python.connection.sync.control_type.class_based import ResourceManagerHandler, S2ControlType

logger = logging.getLogger("s2python")


class BlockingWebsocketClientRM:
    _thread: threading.Thread
    _eventloop: asyncio.AbstractEventLoop
    _control_types: list[S2ControlType]
    _s2_connection: S2SyncConnection

    url: str
    asset_details: AssetDetails

    def __init__(
        self, asset_details: AssetDetails, url: str, control_types: list[S2ControlType]
    ) -> None:
        self.url = url
        self.asset_details = asset_details
        self._thread = threading.Thread(target=self._run)
        self._control_types = control_types

    def _run(self) -> None:
        self._eventloop = asyncio.new_event_loop()

        rm_handler = ResourceManagerHandler(
            asset_details=self.asset_details, control_types=self._control_types
        )

        ws_medium = WebsocketClientMedium(url=self.url, verify_certificate=False)
        self._eventloop.run_until_complete(ws_medium.connect())

        # Configure the S2 connection on top of the websocket connection
        self._s2_connection = S2SyncConnection(medium=ws_medium, eventloop=self._eventloop)
        rm_handler.register_handlers(self._s2_connection)
        logger.debug(
            "Starting synchronous S2 connection event loop in thread %s", self._thread.name
        )
        self._s2_connection.run()
        logger.debug(
            "Synchronous S2 connection event loop in thread %s has stopped", self._thread.name
        )

    def start(self) -> None:
        self._thread.start()

    def wait_till_done(self) -> None:
        self._thread.join()

    def stop(self) -> None:
        """Stops the S2 connection.

        Note: Ensure this method is called from a different thread than the thread running the S2 connection.
        Otherwise it will block waiting on the coroutine _do_stop to terminate successfully but it can't run
        the coroutine. A `RuntimeError` will be raised to prevent the indefinite block.
        """
        logger.info("Stopping the S2 connection...")
        self._s2_connection.stop()
        self._eventloop.stop()
        self.wait_till_done()
        logger.info("Stopped the S2 connection.")
