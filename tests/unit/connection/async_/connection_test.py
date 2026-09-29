"""Tests for async connection task management."""

import asyncio
from typing import AsyncGenerator, Coroutine
import uuid
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock

from s2python.common import ReceptionStatus, ReceptionStatusValues
from s2python.connection.async_.connection import S2AsyncConnection
from s2python.connection.async_.medium.s2_medium import (
    S2AsyncMediumConnection,
    UnparsedMediumData,
)
from s2python.connection.connection_events import ConnectionStarted, ConnectionStopped
from s2python.connection.errors import (
    CouldNotReceiveStatusReceptionError,
    PermanentConnectionError,
)


class _EmptyMessageAsyncMedium(S2AsyncMediumConnection):
    async def is_connected(self) -> bool:
        return True

    async def messages(self) -> AsyncGenerator[UnparsedMediumData, None]:
        empty_messages: tuple[UnparsedMediumData, ...] = ()
        for message in empty_messages:
            yield message

    async def send(self, message: str) -> None:
        pass


class _BlockingReceptionStatusAwaiter:
    def __init__(self) -> None:
        self.waiting = asyncio.Event()
        self.done = asyncio.Event()

    async def wait_for_reception_status(
        self, _: uuid.UUID, __: float
    ) -> ReceptionStatus:  # pyright: ignore [reportReturnType]
        self.waiting.set()
        try:
            await asyncio.Event().wait()
        finally:
            self.done.set()


class _ResultReceptionStatusAwaiter:
    def __init__(self, result) -> None:
        self.result = result

    async def wait_for_reception_status(
        self, _: uuid.UUID, __: float
    ) -> ReceptionStatus:
        if isinstance(self.result, BaseException):
            raise self.result
        return self.result


class _FailingStopConnection(S2AsyncConnection):
    async def _wait_till_stop(self) -> None:
        raise RuntimeError("stop waiter failed")


class _BlockingStopConnection(S2AsyncConnection):
    def __init__(self, medium: S2AsyncMediumConnection) -> None:
        super().__init__(medium)
        self.stop_waiting = asyncio.Event()
        self.stop_waiter_done = asyncio.Event()

    async def _wait_till_stop(self) -> None:
        self.stop_waiting.set()
        try:
            await super()._wait_till_stop()
        finally:
            self.stop_waiter_done.set()


class _RecordingTaskFactory:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.tasks: list[asyncio.Task] = []

    def create_task(self, coroutine: Coroutine) -> asyncio.Task:
        task = self.loop.create_task(coroutine)
        self.tasks.append(task)
        return task


class _LifecycleConnection(S2AsyncConnection):
    def __init__(self, task_factory: _RecordingTaskFactory) -> None:
        super().__init__(_EmptyMessageAsyncMedium(), eventloop=task_factory)  # type: ignore[arg-type]
        self.receive_started = asyncio.Event()
        self.handle_started = asyncio.Event()
        self.receive_done = asyncio.Event()
        self.handle_done = asyncio.Event()

    async def _receive_messages(self) -> None:
        self.receive_started.set()
        try:
            await asyncio.Event().wait()
        finally:
            self.receive_done.set()

    async def _handle_received_messages(self) -> None:
        self.handle_started.set()
        try:
            await asyncio.Event().wait()
        finally:
            self.handle_done.set()


class _FailingReceiveConnection(_LifecycleConnection):
    async def _receive_messages(self) -> None:
        self.receive_started.set()
        self.receive_done.set()
        raise RuntimeError("receive failed")


class AsyncConnectionTest(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.message = Mock()
        self.message.message_id = uuid.uuid4()
        self.message.to_json.return_value = "{}"

    async def wait_for_background_tasks(self, connection: _LifecycleConnection) -> None:
        await connection.receive_started.wait()
        await connection.handle_started.wait()

    def reception_status(
        self, status: ReceptionStatusValues = ReceptionStatusValues.OK
    ):
        return ReceptionStatus(  # pyright: ignore[reportCallIssue]
            subject_message_id=self.message.message_id, status=status
        )

    async def test__send_msg_and_await_reception_status__send_msg_cancellation_drains_reception_status_task(
        self,
    ) -> None:
        # Arrange
        connection = S2AsyncConnection(_EmptyMessageAsyncMedium())
        awaiter = _BlockingReceptionStatusAwaiter()
        connection._reception_status_awaiter = awaiter

        send_task = asyncio.create_task(
            connection.send_msg_and_await_reception_status(self.message)
        )
        await awaiter.waiting.wait()

        # Act
        send_task.cancel()

        # Assert
        with self.assertRaises(asyncio.CancelledError):
            await send_task

        self.assertTrue(awaiter.done.is_set())

    async def test__send_msg_and_await_reception_status__returns_reception_status(
        self,
    ) -> None:
        # Arrange
        connection = _BlockingStopConnection(_EmptyMessageAsyncMedium())
        expected_status = self.reception_status()
        connection._reception_status_awaiter = _ResultReceptionStatusAwaiter(
            expected_status
        )

        # Act
        received_status = await connection.send_msg_and_await_reception_status(
            self.message
        )

        # Assert
        self.assertEqual(expected_status, received_status)
        self.assertTrue(connection.stop_waiter_done.is_set())
        self.assertFalse(connection._stop_event.is_set())

    async def test__send_msg_and_await_reception_status__times_out_and_stops_connection(
        self,
    ) -> None:
        # Arrange
        connection = _BlockingStopConnection(_EmptyMessageAsyncMedium())
        connection._reception_status_awaiter = _ResultReceptionStatusAwaiter(
            asyncio.TimeoutError()
        )

        # Act & Assert
        with self.assertRaises(asyncio.TimeoutError):
            await connection.send_msg_and_await_reception_status(self.message)

        self.assertTrue(connection._stop_event.is_set())
        self.assertTrue(connection.stop_waiter_done.is_set())

    async def test__send_msg_and_await_reception_status__real_timeout_stops_connection(
        self,
    ) -> None:
        connection = S2AsyncConnection(_EmptyMessageAsyncMedium())

        with self.assertRaises(asyncio.TimeoutError):
            await connection.send_msg_and_await_reception_status(
                self.message, timeout_reception_status=0
            )

        self.assertTrue(connection._stop_event.is_set())
        self.assertEqual({}, connection._reception_status_awaiter.awaiting)

    async def test__send_msg_and_await_reception_status__stopping_connection_drains_reception_status_task(
        self,
    ) -> None:
        # Arrange
        connection = S2AsyncConnection(_EmptyMessageAsyncMedium())
        awaiter = _BlockingReceptionStatusAwaiter()
        connection._reception_status_awaiter = awaiter
        send_task = asyncio.create_task(
            connection.send_msg_and_await_reception_status(self.message)
        )
        await awaiter.waiting.wait()

        # Act
        await connection.stop()

        # Assert
        with self.assertRaisesRegex(
            CouldNotReceiveStatusReceptionError,
            "Connection stopped while waiting for ReceptionStatus",
        ):
            await send_task
        self.assertTrue(awaiter.done.is_set())

    async def test__send_msg_and_await_reception_status__send_msg_observes_stop_task_exception(
        self,
    ) -> None:
        # Arrange
        connection = _FailingStopConnection(_EmptyMessageAsyncMedium())
        connection._reception_status_awaiter = _ResultReceptionStatusAwaiter(
            self.reception_status()
        )

        # Act & Assert
        with self.assertRaisesRegex(RuntimeError, "stop waiter failed"):
            await connection.send_msg_and_await_reception_status(self.message)

    async def test__send_msg_and_await_reception_status__propagates_reception_status_exception(
        self,
    ) -> None:
        # Arrange
        connection = _BlockingStopConnection(_EmptyMessageAsyncMedium())
        connection._reception_status_awaiter = _ResultReceptionStatusAwaiter(
            ValueError("reception status waiter failed")
        )

        # Act & Assert
        with self.assertRaisesRegex(ValueError, "reception status waiter failed"):
            await connection.send_msg_and_await_reception_status(self.message)

        self.assertTrue(connection.stop_waiter_done.is_set())

    async def test__send_msg_and_await_reception_status__propagates_child_cancellation(
        self,
    ) -> None:
        # Arrange
        connection = _BlockingStopConnection(_EmptyMessageAsyncMedium())
        connection._reception_status_awaiter = _ResultReceptionStatusAwaiter(
            asyncio.CancelledError()
        )

        # Act & Assert
        with self.assertRaises(asyncio.CancelledError):
            await connection.send_msg_and_await_reception_status(self.message)

        self.assertTrue(connection.stop_waiter_done.is_set())

    async def test__send_msg_and_await_reception_status__raises_on_permanent_error(
        self,
    ) -> None:
        # Arrange
        connection = S2AsyncConnection(_EmptyMessageAsyncMedium())
        permanent_error_status = self.reception_status(
            ReceptionStatusValues.PERMANENT_ERROR
        )
        connection._reception_status_awaiter = _ResultReceptionStatusAwaiter(
            permanent_error_status
        )

        # Act & Assert
        with self.assertRaises(PermanentConnectionError):
            await connection.send_msg_and_await_reception_status(self.message)

    async def test__send_msg_and_await_reception_status__returns_permanent_error_when_raise_on_error_is_false(
        self,
    ) -> None:
        # Arrange
        connection = S2AsyncConnection(_EmptyMessageAsyncMedium())
        permanent_error_status = self.reception_status(
            ReceptionStatusValues.PERMANENT_ERROR
        )
        connection._reception_status_awaiter = _ResultReceptionStatusAwaiter(
            permanent_error_status
        )

        # Act
        received_status = await connection.send_msg_and_await_reception_status(
            self.message, raise_on_error=False
        )

        # Assert
        self.assertEqual(permanent_error_status, received_status)

    async def test__run__graceful_stop_drains_background_tasks(self) -> None:
        # Arrange
        task_factory = _RecordingTaskFactory()
        connection = _LifecycleConnection(task_factory)
        connection._handlers.handle_event = AsyncMock()
        run_task = asyncio.create_task(connection.run())
        await self.wait_for_background_tasks(connection)

        # Act
        await connection.stop()
        await run_task

        # Assert
        self.assertTrue(all(task.done() for task in task_factory.tasks))
        self.assertTrue(connection.receive_done.is_set())
        self.assertTrue(connection.handle_done.is_set())
        handled_events = [
            type(call.args[1])
            for call in connection._handlers.handle_event.await_args_list
        ]
        self.assertEqual([ConnectionStarted, ConnectionStopped], handled_events)

    async def test__run__parent_cancellation_drains_background_tasks(self) -> None:
        # Arrange
        task_factory = _RecordingTaskFactory()
        connection = _LifecycleConnection(task_factory)
        connection._handlers.handle_event = AsyncMock()
        run_task = asyncio.create_task(connection.run())
        await self.wait_for_background_tasks(connection)

        # Act
        run_task.cancel()

        # Assert
        with self.assertRaises(asyncio.CancelledError):
            await run_task
        self.assertTrue(all(task.done() for task in task_factory.tasks))
        self.assertTrue(connection.receive_done.is_set())
        self.assertTrue(connection.handle_done.is_set())

    async def test__run__started_handler_failure_drains_background_tasks(self) -> None:
        # Arrange
        task_factory = _RecordingTaskFactory()
        connection = _LifecycleConnection(task_factory)
        connection._handlers.handle_event = AsyncMock(
            side_effect=RuntimeError("handler failed")
        )

        # Act & Assert
        with self.assertRaisesRegex(RuntimeError, "handler failed"):
            await connection.run()
        self.assertTrue(all(task.done() for task in task_factory.tasks))

    async def test__run__stopped_handler_failure_drains_background_tasks(self) -> None:
        # Arrange
        task_factory = _RecordingTaskFactory()
        connection = _LifecycleConnection(task_factory)

        async def handle_event(_, event) -> None:
            if isinstance(event, ConnectionStopped):
                raise RuntimeError("handler failed")

        connection._handlers.handle_event = handle_event
        run_task = asyncio.create_task(connection.run())
        await self.wait_for_background_tasks(connection)

        # Act
        await connection.stop()

        # Assert
        with self.assertRaisesRegex(RuntimeError, "handler failed"):
            await run_task
        self.assertTrue(all(task.done() for task in task_factory.tasks))
        self.assertTrue(connection.receive_done.is_set())
        self.assertTrue(connection.handle_done.is_set())

    async def test__run__background_failure_drains_remaining_tasks(self) -> None:
        # Arrange
        task_factory = _RecordingTaskFactory()
        connection = _FailingReceiveConnection(task_factory)
        connection._handlers.handle_event = AsyncMock()

        # Act
        with self.assertLogs("s2python", level="ERROR") as logs:
            await connection.run()

        # Assert
        self.assertTrue(all(task.done() for task in task_factory.tasks))
        self.assertTrue(connection.handle_done.is_set())
        self.assertTrue(any("receive failed" in message for message in logs.output))
