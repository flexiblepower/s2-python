from unittest import TestCase

import importlib
import inspect
import pkgutil

from s2python import message
from s2python.validate_values_mixin import S2MessageComponent


class S2MessageTest(TestCase):

    def _test_import_s2_messages(self, module_name):
        """Make sure each S2MessageComponent subclass in the given module is importable from s2_python.message."""
        module = importlib.import_module(module_name)

        # Find all submodules
        all_subclasses = []
        for _, name, is_pkg in pkgutil.iter_modules(module.__path__, module.__name__ + "."):
            submodule = importlib.import_module(name)

            # Find all classes in the submodule that subclass BaseClass
            subclasses = [
                obj for _, obj in inspect.getmembers(submodule, inspect.isclass)
                if issubclass(obj, S2MessageComponent) and obj is not S2MessageComponent
            ]
            all_subclasses.extend(subclasses)

        # Ensure we found at least one subclass
        self.assertGreater(len(all_subclasses), 0, f"No subclasses found in {module_name}")

        for S2MessageClass in all_subclasses:
            assert hasattr(message, S2MessageClass.__name__), f"{S2MessageClass} should be importable from s2_python.message"

    def test_import_s2_messages__common(self):
        self._test_import_s2_messages("s2python.common")

    def test_import_s2_messages__ddbc(self):
        self._test_import_s2_messages("s2python.ddbc")

    def test_import_s2_messages__frbc(self):
        self._test_import_s2_messages("s2python.frbc")

    def test_import_s2_messages__pebc(self):
        self._test_import_s2_messages("s2python.pebc")

    def test_import_s2_messages__ppbc(self):
        self._test_import_s2_messages("s2python.ppbc")
