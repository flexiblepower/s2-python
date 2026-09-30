import unittest

from pydantic import ConfigDict

from s2python.common import Handshake
from s2python.generated.gen_s2 import Handshake as GenHandshake
from s2python.validate_values_mixin import copy_config


class CopyConfigTest(unittest.TestCase):
    def test__copy_config__returns_changed_copy(self) -> None:
        # Arrange
        config = ConfigDict(extra="forbid")

        # Act
        copied = copy_config(config, validate_assignment=True)

        # Assert
        self.assertEqual(copied, {"extra": "forbid", "validate_assignment": True})
        self.assertEqual(config, {"extra": "forbid"})

    def test__copy_config__generated_config_unchanged_by_subclass(self) -> None:
        # Arrange / Act
        # Handshake copies the generated config with validate_assignment=True.
        wrapper_config = Handshake.model_config
        generated_config = GenHandshake.model_config

        # Assert
        self.assertTrue(wrapper_config.get("validate_assignment"))
        self.assertNotIn("validate_assignment", generated_config)
