from typing import Union

from s2python.connection.connection_events import S2ConnectionEvent
from s2python.message import S2MessageWithID


S2ConnectionEventsAndMessages = Union[S2MessageWithID, S2ConnectionEvent]
