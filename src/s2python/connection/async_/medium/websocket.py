import logging
import ssl
from typing import AsyncGenerator, Optional, Dict, Any
from typing_extensions import override

from s2python.s2_parser import UnparsedS2Message

try:
    import websockets
    from websockets.asyncio.client import (
        ClientConnection as WSConnection,
        connect as ws_connect,
    )
except ImportError as exc:
    raise ImportError(
        "The 'websockets' package is required. Run 'pip install s2-python[ws]' to use this feature."
    ) from exc

from s2python.connection.async_.medium.s2_medium import MediumClosedConnectionError, MediumCouldNotConnectError, S2MediumConnection

logger = logging.getLogger("s2python")


class WebsocketClientMedium(S2MediumConnection):
    url: str

    _ws: Optional[WSConnection]
    _verify_certificate: bool
    _bearer_token: Optional[str]
    _closed: bool

    def __init__(self, url: str, verify_certificate: bool = True, bearer_token: Optional[str] = None) -> None:
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

            self.ws = await ws_connect(uri=self.url, **connection_kwargs)
        except (EOFError, OSError, websockets.WebSocketException) as e:
            self._closed = True
            message = f"Could not connect due to: {e}"
            logger.error(message)
            raise MediumCouldNotConnectError(message)

    @override
    async def is_connected(self) -> bool:
        return self.ws is not None and not self._closed

    @override
    async def messages(self) -> AsyncGenerator[UnparsedS2Message, None]:
        try:
            async for message in self.ws:
                yield message
        except websockets.WebSocketException as e:
            self._closed = True
            raise MediumClosedConnectionError(f'Could not receive more messages on websocket connection {self.url}') from e

    @override
    async def send(self, message: str) -> None:
        try:
            await self.ws.send(message)
        except websockets.WebSocketException as e:
            self._closed = True
            raise MediumClosedConnectionError(f'Could not send message {message}') from e
