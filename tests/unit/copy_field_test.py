import unittest

from s2python.ddbc import DDBCOperationMode
from s2python.generated.gen_s2 import DDBCOperationMode as GenDDBCOperationMode, ID
from s2python.validate_values_mixin import copy_field


class CopyFieldTest(unittest.TestCase):
    def test__copy_field__returns_equal_copy(self) -> None:
        # Arrange
        field = GenDDBCOperationMode.model_fields["diagnostic_label"]

        # Act
        copied = copy_field(field)

        # Assert
        self.assertIsNot(copied, field)
        self.assertEqual(copied.annotation, field.annotation)
        self.assertEqual(copied.description, field.description)

    def test__copy_field__generated_field_unchanged_by_subclass(self) -> None:
        # Arrange / Act
        # DDBCOperationMode redefines the generated field 'Id' as 'id' with type uuid.UUID.
        wrapper_field = DDBCOperationMode.model_fields["id"]
        generated_field = GenDDBCOperationMode.model_fields["Id"]

        # Assert
        self.assertIsNot(wrapper_field, generated_field)
        self.assertIs(generated_field.annotation, ID)
