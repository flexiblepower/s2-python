from typing import List
from unittest import TestCase

from s2python.utils import pairwise


class PairwiseTest(TestCase):
    def test_empty(self):
        # Arrange
        input_array: List[int] = []

        # Act
        pairs = list(pairwise(input_array))

        # Assert
        self.assertEqual(len(pairs), 0)

    def test_len_2(self):
        # Arrange
        input_array = [1, 2]

        # Act
        pairs = list(pairwise(input_array))

        # Assert
        self.assertEqual(pairs, [(1, 2)])

    def test_odd(self):
        # Arrange
        input_array = [1, 2, 3]

        # Act
        pairs = list(pairwise(input_array))

        # Assert
        self.assertEqual(pairs, [(1, 2), (2, 3)])

    def test_even(self):
        # Arrange
        input_array = [1, 2, 3, 4]

        # Act
        pairs = list(pairwise(input_array))

        # Assert
        self.assertEqual(pairs, [(1, 2), (2, 3), (3, 4)])
