import unittest

from s2python.s2_base_model import S2BaseModel


class S2BaseModelTest(unittest.TestCase):
    def test__s2_base_model__validator_built_on_first_use(self) -> None:
        # Arrange
        class ExampleModel(S2BaseModel):
            value: int

        built_before_use = ExampleModel.__pydantic_complete__

        # Act
        example = ExampleModel(value=1)

        # Assert
        self.assertFalse(built_before_use)
        self.assertTrue(ExampleModel.__pydantic_complete__)
        self.assertEqual(example.value, 1)
