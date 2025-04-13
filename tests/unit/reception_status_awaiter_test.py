"""Tests for ReceptionStatusAwaiter.

Copied from
https://github.com/flexiblepower/s2-analyzer/blob/main/backend/test/s2_analyzer_backend/reception_status_awaiter_test.py
under Apache2 license on 31-08-2024.
"""

import asyncio
import datetime
import uuid
from unittest import IsolatedAsyncioTestCase

from s2python.common import (
    ReceptionStatus,
    ReceptionStatusValues,
    InstructionStatus,
    InstructionStatusUpdate,
)
from s2python.reception_status_awaiter import ReceptionStatusAwaiter


class ReceptionStatusAwaiterTest(IsolatedAsyncioTestCase):
    async def test__wait_for_reception_status__receive_while_waiting(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        message_id = uuid.uuid4()
        s2_reception_status = ReceptionStatus(  # pyright: ignore[reportCallIssue]
            subject_message_id=message_id, status=ReceptionStatusValues.OK
        )

        # Act
        wait_task = asyncio.create_task(
            awaiter.wait_for_reception_status(message_id, 1.0)
        )
        should_be_waiting_still = not wait_task.done()
        await awaiter.receive_reception_status(s2_reception_status)
        await wait_task
        received_s2_reception_status = wait_task.result()

        # Assert
        expected_s2_reception_status = ReceptionStatus(  # pyright: ignore[reportCallIssue]
            subject_message_id=message_id, status=ReceptionStatusValues.OK
        )

        self.assertTrue(should_be_waiting_still)
        self.assertEqual(expected_s2_reception_status, received_s2_reception_status)

    async def test__wait_for_reception_status__already_received(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        message_id = uuid.uuid4()
        s2_reception_status = ReceptionStatus(  # pyright: ignore[reportCallIssue]
            subject_message_id=message_id, status=ReceptionStatusValues.OK
        )

        # Act
        await awaiter.receive_reception_status(s2_reception_status)
        received_s2_reception_status = await awaiter.wait_for_reception_status(
            message_id, 1.0
        )

        # Assert
        expected_s2_reception_status = ReceptionStatus(  # pyright: ignore[reportCallIssue]
            subject_message_id=message_id, status=ReceptionStatusValues.OK
        )
        self.assertEqual(expected_s2_reception_status, received_s2_reception_status)

    async def test__wait_for_reception_status__multiple_receive_while_waiting(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        message_id = uuid.uuid4()
        s2_reception_status = ReceptionStatus(  # pyright: ignore[reportCallIssue]
            subject_message_id=message_id, status=ReceptionStatusValues.OK
        )

        # Act
        wait_task_1 = asyncio.create_task(
            awaiter.wait_for_reception_status(message_id, 1.0)
        )
        wait_task_2 = asyncio.create_task(
            awaiter.wait_for_reception_status(message_id, 1.0)
        )
        should_be_waiting_still_1 = not wait_task_1.done()
        should_be_waiting_still_2 = not wait_task_2.done()
        await awaiter.receive_reception_status(s2_reception_status)
        await wait_task_1
        await wait_task_2
        received_s2_reception_status_1 = wait_task_1.result()
        received_s2_reception_status_2 = wait_task_2.result()

        # Assert
        expected_s2_reception_status = ReceptionStatus(  # pyright: ignore[reportCallIssue]
            subject_message_id=message_id, status=ReceptionStatusValues.OK
        )

        self.assertTrue(should_be_waiting_still_1)
        self.assertTrue(should_be_waiting_still_2)
        self.assertEqual(expected_s2_reception_status, received_s2_reception_status_1)
        self.assertEqual(expected_s2_reception_status, received_s2_reception_status_2)

    async def test__receive_reception_status__wrong_message(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        s2_msg = InstructionStatusUpdate(
            message_id=uuid.uuid4(),
            instruction_id=uuid.uuid4(),
            status_type=InstructionStatus.NEW,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
        )

        # Act / Assert
        with self.assertRaises(RuntimeError):
            await awaiter.receive_reception_status(s2_msg)  # type: ignore[arg-type]

    async def test__receive_reception_status__received_duplicate(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        s2_reception_status = ReceptionStatus(  # pyright: ignore[reportCallIssue]
            subject_message_id=uuid.uuid4(), status=ReceptionStatusValues.OK
        )

        # Act / Assert
        await awaiter.receive_reception_status(s2_reception_status)
        with self.assertRaises(RuntimeError):
            await awaiter.receive_reception_status(s2_reception_status)

    async def test__receive_reception_status__receive_no_awaiting(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        message_id = uuid.uuid4()
        s2_reception_status = ReceptionStatus(  # pyright: ignore[reportCallIssue]
            subject_message_id=message_id, status=ReceptionStatusValues.OK
        )

        # Act
        await awaiter.receive_reception_status(s2_reception_status)

        # Assert
        expected_received = {
            message_id: ReceptionStatus(  # pyright: ignore[reportCallIssue]
                subject_message_id=message_id, status=ReceptionStatusValues.OK
            )
        }
        self.assertEqual(awaiter.received, expected_received)
        self.assertEqual(awaiter.awaiting, {})

    async def test__receive_reception_status__receive_with_awaiting(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        awaiting_event = asyncio.Event()
        message_id = uuid.uuid4()
        awaiter.awaiting = {message_id: awaiting_event}
        s2_reception_status = ReceptionStatus(  # pyright: ignore[reportCallIssue]
            subject_message_id=message_id, status=ReceptionStatusValues.OK
        )

        # Act
        should_not_be_set = not awaiting_event.is_set()
        await awaiter.receive_reception_status(s2_reception_status)
        should_be_set = awaiting_event.is_set()

        # Assert
        expected_received = {
            message_id: ReceptionStatus(  # pyright: ignore[reportCallIssue]
                subject_message_id=message_id, status=ReceptionStatusValues.OK
            )
        }

        self.assertTrue(should_not_be_set)
        self.assertTrue(should_be_set)
        self.assertEqual(awaiter.received, expected_received)
        self.assertEqual(awaiter.awaiting, {})
