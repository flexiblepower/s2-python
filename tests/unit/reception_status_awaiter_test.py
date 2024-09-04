"""Tests for ReceptionStatusAwaiter.

Copied from https://github.com/flexiblepower/s2-analyzer/blob/main/backend/test/s2_analyzer_backend/reception_status_awaiter_test.py under Apache2 license on 31-08-2024.
"""

import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock

from s2python.reception_status_awaiter import ReceptionStatusAwaiter


class ReceptionStatusAwaiterTest(IsolatedAsyncioTestCase):
    async def test__wait_for_reception_status__receive_while_waiting(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        message_id = "1"
        s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": message_id,
            "status": "OK",
        }

        # Act
        wait_task = asyncio.create_task(awaiter.wait_for_reception_status(message_id))
        should_be_waiting_still = not wait_task.done()
        await awaiter.receive_reception_status(s2_reception_status)
        await wait_task
        received_s2_reception_status = wait_task.result()

        # Assert
        expected_s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": "1",
            "status": "OK",
        }

        self.assertTrue(should_be_waiting_still)
        self.assertEqual(expected_s2_reception_status, received_s2_reception_status)

    async def test__wait_for_reception_status__already_received(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        message_id = "1"
        s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": message_id,
            "status": "OK",
        }

        # Act
        await awaiter.receive_reception_status(s2_reception_status)
        received_s2_reception_status = await awaiter.wait_for_reception_status(message_id)

        # Assert
        expected_s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": "1",
            "status": "OK",
        }
        self.assertEqual(expected_s2_reception_status, received_s2_reception_status)

    async def test__wait_for_reception_status__multiple_receive_while_waiting(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        message_id = "1"
        s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": message_id,
            "status": "OK",
        }

        # Act
        wait_task_1 = asyncio.create_task(awaiter.wait_for_reception_status(message_id))
        wait_task_2 = asyncio.create_task(awaiter.wait_for_reception_status(message_id))
        should_be_waiting_still_1 = not wait_task_1.done()
        should_be_waiting_still_2 = not wait_task_2.done()
        await awaiter.receive_reception_status(s2_reception_status)
        await wait_task_1
        await wait_task_2
        received_s2_reception_status_1 = wait_task_1.result()
        received_s2_reception_status_2 = wait_task_2.result()

        # Assert
        expected_s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": "1",
            "status": "OK",
        }

        self.assertTrue(should_be_waiting_still_1)
        self.assertTrue(should_be_waiting_still_2)
        self.assertEqual(expected_s2_reception_status, received_s2_reception_status_1)
        self.assertEqual(expected_s2_reception_status, received_s2_reception_status_2)

    async def test__receive_reception_status__wrong_message(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        s2_msg = {"message_type": "NotAReceptionStatus", "subject_message_id": "1", "status": "OK"}

        # Act / Assert
        with self.assertRaises(RuntimeError):
            await awaiter.receive_reception_status(s2_msg)

    async def test__receive_reception_status__received_duplicate(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": "1",
            "status": "OK",
        }

        # Act / Assert
        await awaiter.receive_reception_status(s2_reception_status)
        with self.assertRaises(RuntimeError):
            await awaiter.receive_reception_status(s2_reception_status)

    async def test__receive_reception_status__receive_no_awaiting(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": "1",
            "status": "OK",
        }

        # Act
        await awaiter.receive_reception_status(s2_reception_status)

        # Assert
        expected_received = {
            "1": {"message_type": "ReceptionStatus", "subject_message_id": "1", "status": "OK"}
        }
        self.assertEqual(awaiter.received, expected_received)
        self.assertEqual(awaiter.awaiting, {})

    async def test__receive_reception_status__receive_with_awaiting(self):
        # Arrange
        awaiter = ReceptionStatusAwaiter()
        awaiting_event = asyncio.Event()
        awaiter.awaiting = {"1": awaiting_event}
        s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": "1",
            "status": "OK",
        }

        # Act
        should_not_be_set = not awaiting_event.is_set()
        await awaiter.receive_reception_status(s2_reception_status)
        should_be_set = awaiting_event.is_set()

        # Assert
        expected_received = {
            "1": {"message_type": "ReceptionStatus", "subject_message_id": "1", "status": "OK"}
        }

        self.assertTrue(should_not_be_set)
        self.assertTrue(should_be_set)
        self.assertEqual(awaiter.received, expected_received)
        self.assertEqual(awaiter.awaiting, {})

    async def test__send_and_await_reception_status__receive_while_waiting(self):
        # Arrange
        conn = Mock()
        awaiter = ReceptionStatusAwaiter()
        message_id = "1"
        s2_message = {
            "message_type": "Handshake",
            "message_id": message_id,
            "role": "RM",
            "supported_protocol_versions": ["1.0"],
        }
        s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": message_id,
            "status": "OK",
        }

        # Act
        wait_task = asyncio.create_task(
            awaiter.send_and_await_reception_status(conn, s2_message, True)
        )
        should_be_waiting_still = not wait_task.done()
        await awaiter.receive_reception_status(s2_reception_status)
        await wait_task
        received_s2_reception_status = wait_task.result()

        # Assert
        expected_s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": "1",
            "status": "OK",
        }

        self.assertTrue(should_be_waiting_still)
        self.assertEqual(expected_s2_reception_status, received_s2_reception_status)

    async def test__send_and_await_reception_status__receive_while_waiting_not_okay(self):
        # Arrange
        conn = Mock()
        awaiter = ReceptionStatusAwaiter()
        message_id = "1"
        s2_message = {
            "message_type": "Handshake",
            "message_id": message_id,
            "role": "RM",
            "supported_protocol_versions": ["1.0"],
        }
        s2_reception_status = {
            "message_type": "ReceptionStatus",
            "subject_message_id": message_id,
            "status": "INVALID_MESSAGE",
        }

        # Act / Assert
        wait_task = asyncio.create_task(
            awaiter.send_and_await_reception_status(conn, s2_message, True)
        )
        await awaiter.receive_reception_status(s2_reception_status)

        with self.assertRaises(RuntimeError):
            await wait_task
