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
    received: Dict[uuid.UUID, ReceptionStatus]
    awaiting: Dict[uuid.UUID, asyncio.Event]

    def __init__(self) -> None:
        self.received = {}
        self.awaiting = {}

    async def wait_for_reception_status(
        self, message_id: uuid.UUID, timeout_reception_status: float
    ) -> ReceptionStatus:
        if message_id in self.received:
            reception_status = self.received[message_id]
        else:
            if message_id in self.awaiting:
                received_event = self.awaiting[message_id]
            else:
                received_event = asyncio.Event()
                self.awaiting[message_id] = received_event

            await asyncio.wait_for(received_event.wait(), timeout_reception_status)
            reception_status = self.received[message_id]

            if message_id in self.awaiting:
                del self.awaiting[message_id]

        return reception_status

    async def receive_reception_status(self, reception_status: ReceptionStatus) -> None:
        if not isinstance(reception_status, ReceptionStatus):
            raise RuntimeError(
                f"Expected a ReceptionStatus but received message {reception_status}"
            )

        if reception_status.subject_message_id in self.received:
            raise RuntimeError(
                f"ReceptationStatus for message_subject_id {reception_status.subject_message_id} has already "
                f"been received!"
            )

        self.received[reception_status.subject_message_id] = reception_status
        awaiting = self.awaiting.get(reception_status.subject_message_id)

        if awaiting:
            awaiting.set()
            del self.awaiting[reception_status.subject_message_id]
