import logging
import ssl
from types import TracebackType
from typing import AsyncGenerator, Optional, Dict, Any
from typing_extensions import override

from s2python.connection.async_.medium.s2_medium import (
    MediumClosedConnectionError,
    MediumCouldNotConnectError,
    S2AsyncMediumConnection,
    UnparsedMediumData,
)

try:
    import websockets
    from websockets.asyncio.client import (
        ClientConnection as WSConnection,
        connect as ws_connect,
    )
    from websockets import Data
except ImportError as exc:
    raise ImportError(
        "The 'websockets' package is required. Run 'pip install s2-python[ws]' to use this feature."
    ) from exc

logger = logging.getLogger("s2python")


class WebsocketClientMedium(S2AsyncMediumConnection):
    url: str

    _ws: Optional[WSConnection]
    _verify_certificate: bool
    _bearer_token: Optional[str]
    _closed: bool

    def __init__(
        self, url: str, verify_certificate: bool = True, bearer_token: Optional[str] = None
    ) -> None:
        """Construct a Websocket client medium.

        :param url: The websocket url to connect to.
        :param verify_certificate: If we should verify the TLS certificate.
        IF SET TO FALSE THERE IS NO GUARANTEE THE CONNECTION IS SECURE. USE WITH CAUTION.
        :param bearer_token: Security token set in the 'Authorization' header as 'Bearer {token}' if provided.
        """
        self.url = url

        self._ws = None
        self._verify_certificate = verify_certificate
        self._bearer_token = bearer_token
        self._closed = False

    async def connect(self) -> None:
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

            self._ws = await ws_connect(uri=self.url, **connection_kwargs)
        except (EOFError, OSError, websockets.WebSocketException) as e:
            self._closed = True
            message = f"Could not connect due to: {e}"
            logger.error(message)
            raise MediumCouldNotConnectError(message) from e

    async def disconnect(self) -> None:
        if self._ws is not None:
            await self._ws.close()
            self._closed = True

    async def __aenter__(self) -> "WebsocketClientMedium":
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.disconnect()

    @override
    async def is_connected(self) -> bool:
        return self._ws is not None and not self._closed

    @override
    async def messages(  # pylint: disable=invalid-overridden-method
        self,
    ) -> AsyncGenerator[UnparsedMediumData, None]:
        if self._ws is None:
            raise RuntimeError("Websocket is not connected")
        try:
            message: Data
            async for message in self._ws:
                yield message
        except websockets.WebSocketException as e:
            self._closed = True
            raise MediumClosedConnectionError(
                f"Could not receive more messages on websocket connection {self.url}"
            ) from e

    @override
    async def send(self, message: str) -> None:
        if self._ws is None:
            raise RuntimeError("Websocket is not connected")
        try:
            await self._ws.send(message)
        except websockets.WebSocketException as e:
            self._closed = True
            raise MediumClosedConnectionError(f"Could not send message {message}") from e
