import json
from unittest import TestCase

from s2python.common import Role, Commodity, RoleType


class RoleTest(TestCase):
    def test__from_json__happy_path(self):
        # Arrange
        json_str = '{"commodity": "HEAT", "role": "ENERGY_STORAGE"}'

        # Act
        role: Role = Role.from_json(json_str)

        # Assert
        self.assertEqual(role.commodity, Commodity.HEAT)
        self.assertEqual(role.role, RoleType.ENERGY_STORAGE)

    def test__to_json__happy_path(self):
        # Arrange
        role = Role(commodity=Commodity.HEAT, role=RoleType.ENERGY_STORAGE)

        # Act
        json_str = role.to_json()

        # Assert
        expected_json = {"commodity": "HEAT", "role": "ENERGY_STORAGE"}
        self.assertEqual(json.loads(json_str), expected_json)
