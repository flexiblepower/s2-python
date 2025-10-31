from s2python.connection.connection_events import S2ConnectionEvent

from typing import Callable, Union, Coroutine, Any, Optional

from s2python.message import S2MessageWithID


S2ConnectionEventsAndMessages = Union[S2MessageWithID, S2ConnectionEvent]
