import threading
import asyncio
from typing import Optional
from s2python.communication.s2_connection import S2Connection
from s2python.common import EnergyManagementRole

class CustomThreadS2Connection(S2Connection):
    """
    Extends S2Connection to allow running the event loop in a developer-supplied thread.

    If a thread is provided, the event loop will be run in that thread. The developer is responsible
    for managing the thread's lifecycle and ensuring it is not used for other conflicting tasks.
    """
    def __init__(self, *args, thread: Optional[threading.Thread] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._external_thread = thread
        self._thread_started_by_user = False

    def start(self) -> None:
        if self._external_thread:
            # Only start the thread if it is not already running
            if not self._external_thread.is_alive():
                def run_loop():
                    asyncio.set_event_loop(self._eventloop)
                    if self.role == EnergyManagementRole.RM:
                        self._run_eventloop(self._run_as_rm())
                    else:
                        self._run_eventloop(self._run_as_cem())
                self._external_thread.run = run_loop
                self._external_thread.start()
                self._thread_started_by_user = True
            else:
                raise RuntimeError("Provided thread is already running. Please provide a fresh thread.")
        else:
            # Default behavior: run in the current thread
            super().start()

    def stop(self) -> None:
        """
        Stops the S2 connection. If an external thread was provided and started by this class,
        it will join that thread. Otherwise, uses the default stop behavior.
        """
        if self._external_thread and self._thread_started_by_user:
            if self._eventloop.is_running():
                asyncio.run_coroutine_threadsafe(self._do_stop(), self._eventloop).result()
            self._external_thread.join()
        else:
            super().stop() 
