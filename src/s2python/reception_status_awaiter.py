"""ReceptationStatusAwaiter class which notifies any coroutine waiting for a certain reception status message.

Copied from
https://github.com/flexiblepower/s2-analyzer/blob/main/backend/s2_analyzer_backend/reception_status_awaiter.py under
Apache2 license on 31-08-2024.
"""

import asyncio
import uuid
from typing import Dict

from s2python.common import ReceptionStatus


class ReceptionStatusAwaiter:
    """Notify coroutines waiting for a `ReceptionStatus` by subject message ID.

    Reception statuses are single-consumer: once awaited, they are removed."""

    received: Dict[uuid.UUID, ReceptionStatus]
    awaiting: Dict[uuid.UUID, asyncio.Event]

    def __init__(self) -> None:
        self.received = {}
        self.awaiting = {}

    async def wait_for_reception_status(
        self, message_id: uuid.UUID, timeout_reception_status: float
    ) -> ReceptionStatus:

        existing = self.received.pop(message_id, None)
        if existing is not None:
            return existing

        received_event = self.awaiting.get(message_id)
        if received_event is None:
            received_event = asyncio.Event()
            self.awaiting[message_id] = received_event

        try:
            await asyncio.wait_for(received_event.wait(), timeout_reception_status)
            return self.received.pop(message_id)
        finally:
            self.awaiting.pop(message_id, None)

    async def receive_reception_status(self, reception_status: ReceptionStatus) -> None:
        if not isinstance(reception_status, ReceptionStatus):
            raise RuntimeError(
                f"Expected a ReceptionStatus but received message {reception_status}"
            )

        mid = reception_status.subject_message_id

        if mid in self.received:
            raise RuntimeError(
                f"ReceptionStatus for message_subject_id {mid} has already been received!"
            )

        self.received[mid] = reception_status

        awaiting = self.awaiting.get(mid)
        if awaiting is not None:
            awaiting.set()
            self.awaiting.pop(mid, None)
