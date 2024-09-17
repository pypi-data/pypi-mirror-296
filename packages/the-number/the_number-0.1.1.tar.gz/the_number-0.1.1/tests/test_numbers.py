from __future__ import annotations

import unittest
from typing import Any

from the_number import isFinite, isInf, isInteger, isNaN, isNumber


class TestNumberTypeCheckers(unittest.TestCase):
    def run_test_cases(
        self, func: callable, test_cases: list[tuple[Any, bool]],
    ) -> None:
        """Helper method to run test cases for a given function.

        Args:
        ----
            func (callable): The function to test.
            test_cases (list[tuple[Any, bool]]): List of tuples containing input and expected output.

        """
        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                assert func(input_value) == expected_output

    def test_isInteger(self) -> None:
        """Test the isInteger function with various input types, including complex numbers."""
        test_cases = [
            (1, True),
            (1.0, True),
            (1 + 0j, True),
            (1 + 2j, True),
            (1.5, True),
            (1.5 + 0.5j, True),
            ("1", False),
            ([1], False),
            (None, False),
        ]
        self.run_test_cases(isInteger, test_cases)

    def test_isInf(self) -> None:
        """Test the isInf function with infinite and non-infinite values, including complex numbers."""
        inf = float("inf")
        nan = float("nan")
        test_cases = [
            (inf, True),
            (-inf, True),
            (1, False),
            (0, False),
            (1.5, False),
            (nan, False),
            (1 + 1j, False),
            (inf + 1j, False),  # Complex infinity is not considered infinite
            (1 + inf * 1j, False),
            (complex(inf, inf), False),
        ]
        self.run_test_cases(isInf, test_cases)

    def test_isNaN(self) -> None:
        """Test the isNaN function with NaN and non-NaN values, including complex numbers."""
        inf = float("inf")
        nan = float("nan")
        test_cases = [
            (nan, True),
            (inf, False),
            (-inf, False),
            (1, False),
            (0, False),
            (1.5, False),
            (1 + 1j, False),
            (complex(nan, 0), False),  # Complex NaN is not considered NaN
            (complex(0, nan), False),
            (complex(nan, nan), False),
        ]
        self.run_test_cases(isNaN, test_cases)

    def test_isFinite(self) -> None:
        """Test the isFinite function with finite and infinite numbers, including complex numbers."""
        inf = float("inf")
        nan = float("nan")
        test_cases = [
            (1, True),
            (1.0, True),
            (-1.5, True),
            (1 + 2j, True),
            (1.5 + 0.5j, True),
            (inf, False),
            (-inf, False),
            (nan, False),
            (1 + 1j * inf, False),
            (inf + 1j, False),
            ("1", False),
            (1 + 1j * nan, False),
            (nan + inf * 1j, False),
            (nan + nan * 1j, False),
            (complex(inf, inf), False),
            (complex(nan, nan), False),
        ]
        self.run_test_cases(isFinite, test_cases)


    def test_isNumber(self) -> None:
        """Test the isNumber function with various numeric and non-numeric inputs, including complex numbers."""
        inf = float("inf")
        nan = float("nan")
        test_cases = [
            (1, True),
            (1.0, True),
            (-1.5, True),
            (1 + 2j, True),
            (1.5 + 0.5j, True),
            (inf, True),
            (-inf, True),
            (nan, False),
            ("1", False),
            ([1], False),
            (None, False),
            (1 + 1j * inf, True),
            (1 + 1j * nan, True),
            (nan + inf * 1j, True),
            (complex(inf, inf), True),
            (complex(nan, 0), True),
            (complex(0, nan), True),
            (complex(nan, nan), True),
        ]
        self.run_test_cases(isNumber, test_cases)


if __name__ == "__main__":
    unittest.main()
