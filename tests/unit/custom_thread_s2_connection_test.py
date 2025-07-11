import unittest
import threading
import time
from s2python.communication.custom_thread_s2_connection import CustomThreadS2Connection
from s2python.common import EnergyManagementRole

class DummyS2Connection(CustomThreadS2Connection):
    def _run_eventloop(self, main_task):
        # Simulate event loop running for a short time
        time.sleep(0.1)
    def _run_as_rm(self):
        # Dummy awaitable
        class DummyAwaitable:
            def __await__(self):
                yield
        return DummyAwaitable()
    def _run_as_cem(self):
        class DummyAwaitable:
            def __await__(self):
                yield
        return DummyAwaitable()
    async def _do_stop(self):
        pass

class TestCustomThreadS2Connection(unittest.TestCase):
    def test_start_with_external_thread(self):
        thread = threading.Thread()
        conn = DummyS2Connection(
            url="ws",
            role=EnergyManagementRole.RM,
            thread=thread
        )
        conn.start()
        # Wait for thread to finish
        conn.stop()
        self.assertFalse(thread.is_alive())

    def test_start_without_external_thread(self):
        conn = DummyS2Connection(
            url="ws://localhost:1234",
            role=EnergyManagementRole.CEM
        )
        # Should not raise
        conn.start()
        conn.stop()

if __name__ == "__main__":
    unittest.main() 
