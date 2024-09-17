import sys
import os
import unittest

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from standlib.double import Double

class TestDouble(unittest.TestCase):

    def test_addition(self) -> None:
        a = Double(1.5)
        b = Double(2.5)
        result = a + b
        self.assertEqual(str(result), "4.00000000000000000000000000000000000000000000000000")

    def test_subtraction(self) -> None:
        a = Double(5.5)
        b = Double(2.5)
        result = a - b
        self.assertEqual(str(result), "3.00000000000000000000000000000000000000000000000000")

    def test_multiplication(self) -> None:
        a = Double(3.0)
        b = Double(2.0)
        result = a * b
        self.assertEqual(str(result), "6.00000000000000000000000000000000000000000000000000")

    def test_truedivision(self) -> None:
        a = Double(5.0)
        b = Double(2.0)
        result = a / b
        self.assertEqual(str(result), "2.50000000000000000000000000000000000000000000000000")

    def test_modulo(self) -> None:
        a = Double(5.0)
        b = Double(2.0)
        result = a % b
        self.assertEqual(str(result), "1.00000000000000000000000000000000000000000000000000")

    def test_exponentiation(self) -> None:
        a = Double(2.0)
        b = Double(3.0)
        result = a ** b
        self.assertEqual(str(result), "8.00000000000000000000000000000000000000000000000000")

    def test_floordivision(self) -> None:
        a = Double(5.0)
        b = Double(2.0)
        result = a // b
        self.assertEqual(str(result), "2.00000000000000000000000000000000000000000000000000")

if __name__ == "__main__":
    unittest.main()
