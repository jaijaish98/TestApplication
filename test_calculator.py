#!/usr/bin/env python3
"""
Test script for the Python Calculator Application
Tests all functionality including edge cases and error handling.
"""

import unittest
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Test cases for the Calculator class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()
    
    def test_addition(self):
        """Test addition operations."""
        self.assertEqual(self.calc.calculate("5 + 3"), 8)
        self.assertEqual(self.calc.calculate("10.5 + 2.3"), 12.8)
        self.assertEqual(self.calc.calculate("-5 + 3"), -2)
        self.assertEqual(self.calc.calculate("-5 + -3"), -8)
        self.assertEqual(self.calc.calculate("0 + 0"), 0)
    
    def test_subtraction(self):
        """Test subtraction operations."""
        self.assertEqual(self.calc.calculate("10 - 3"), 7)
        self.assertEqual(self.calc.calculate("5.5 - 2.2"), 3.3)
        self.assertEqual(self.calc.calculate("-5 - 3"), -8)
        self.assertEqual(self.calc.calculate("3 - -5"), 8)
        self.assertEqual(self.calc.calculate("0 - 5"), -5)
    
    def test_multiplication(self):
        """Test multiplication operations."""
        self.assertEqual(self.calc.calculate("5 * 3"), 15)
        self.assertEqual(self.calc.calculate("2.5 * 4"), 10)
        self.assertEqual(self.calc.calculate("-5 * 3"), -15)
        self.assertEqual(self.calc.calculate("-5 * -3"), 15)
        self.assertEqual(self.calc.calculate("0 * 100"), 0)
    
    def test_division(self):
        """Test division operations."""
        self.assertEqual(self.calc.calculate("15 / 3"), 5)
        self.assertEqual(self.calc.calculate("10 / 4"), 2.5)
        self.assertEqual(self.calc.calculate("-15 / 3"), -5)
        self.assertEqual(self.calc.calculate("-15 / -3"), 5)
        self.assertEqual(self.calc.calculate("0 / 5"), 0)
    
    def test_division_by_zero(self):
        """Test division by zero error handling."""
        with self.assertRaises(ZeroDivisionError):
            self.calc.calculate("5 / 0")
        
        with self.assertRaises(ZeroDivisionError):
            self.calc.calculate("-10 / 0")
    
    def test_exponentiation(self):
        """Test exponentiation operations."""
        self.assertEqual(self.calc.calculate("2 ** 3"), 8)
        self.assertEqual(self.calc.calculate("3 ^ 2"), 9)
        self.assertEqual(self.calc.calculate("5 ** 0"), 1)
        self.assertEqual(self.calc.calculate("0 ** 5"), 0)
        self.assertEqual(self.calc.calculate("-2 ** 2"), 4)
        self.assertAlmostEqual(self.calc.calculate("4 ** 0.5"), 2.0, places=10)
    
    def test_decimal_numbers(self):
        """Test operations with decimal numbers."""
        self.assertAlmostEqual(self.calc.calculate("3.14 + 2.86"), 6.0, places=10)
        self.assertAlmostEqual(self.calc.calculate("10.5 - 3.2"), 7.3, places=10)
        self.assertAlmostEqual(self.calc.calculate("2.5 * 4.2"), 10.5, places=10)
        self.assertAlmostEqual(self.calc.calculate("7.5 / 2.5"), 3.0, places=10)
    
    def test_negative_numbers(self):
        """Test operations with negative numbers."""
        self.assertEqual(self.calc.calculate("-5 + 3"), -2)
        self.assertEqual(self.calc.calculate("-10 - -5"), -5)
        self.assertEqual(self.calc.calculate("-4 * -3"), 12)
        self.assertEqual(self.calc.calculate("-15 / -3"), 5)
        self.assertEqual(self.calc.calculate("-2 ** 3"), -8)
    
    def test_invalid_expressions(self):
        """Test error handling for invalid expressions."""
        invalid_expressions = [
            "5 +",           # Missing operand
            "+ 3",           # Missing operand
            "5 + 3 + 2",     # Too many operands
            "5 & 3",         # Invalid operator
            "abc + 3",       # Invalid number
            "5 + def",       # Invalid number
            "",              # Empty string
            "5 ++ 3",        # Invalid operator
            "5.5.5 + 3",     # Invalid number format
        ]
        
        for expr in invalid_expressions:
            with self.assertRaises(ValueError, msg=f"Should raise ValueError for: {expr}"):
                self.calc.calculate(expr)
    
    def test_parse_expression(self):
        """Test expression parsing functionality."""
        # Valid expressions
        self.assertEqual(self.calc.parse_expression("5 + 3"), (5.0, '+', 3.0))
        self.assertEqual(self.calc.parse_expression("-5 * 3"), (-5.0, '*', 3.0))
        self.assertEqual(self.calc.parse_expression("10.5 / -2.5"), (10.5, '/', -2.5))
        self.assertEqual(self.calc.parse_expression("2 ** 3"), (2.0, '**', 3.0))
        
        # Test with extra whitespace
        self.assertEqual(self.calc.parse_expression("  5   +   3  "), (5.0, '+', 3.0))
    
    def test_format_result(self):
        """Test result formatting."""
        self.assertEqual(self.calc.format_result(5), "5")
        self.assertEqual(self.calc.format_result(5.0), "5")
        self.assertEqual(self.calc.format_result(5.5), "5.5")
        self.assertEqual(self.calc.format_result(3.14159), "3.14159")
    
    def test_large_numbers(self):
        """Test operations with large numbers."""
        self.assertEqual(self.calc.calculate("1000000 + 2000000"), 3000000)
        self.assertEqual(self.calc.calculate("1000000 * 1000"), 1000000000)
    
    def test_very_small_numbers(self):
        """Test operations with very small numbers."""
        result = self.calc.calculate("0.0001 + 0.0002")
        self.assertAlmostEqual(result, 0.0003, places=10)
        
        result = self.calc.calculate("0.1 * 0.1")
        self.assertAlmostEqual(result, 0.01, places=10)


class TestCalculatorIntegration(unittest.TestCase):
    """Integration tests for the calculator application."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()
    
    def test_calculator_workflow(self):
        """Test a typical calculator workflow."""
        # Test a series of calculations
        test_cases = [
            ("5 + 3", 8),
            ("10 - 4", 6),
            ("6 * 7", 42),
            ("15 / 3", 5),
            ("2 ** 3", 8),
            ("3 ^ 2", 9),
        ]
        
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result = self.calc.calculate(expression)
                self.assertEqual(result, expected)


def run_manual_tests():
    """Run manual tests to demonstrate calculator functionality."""
    print("🧪 Running Manual Calculator Tests")
    print("=" * 50)
    
    calc = Calculator()
    
    test_expressions = [
        "5 + 3",
        "10.5 - 2.3",
        "-4 * 6",
        "15 / 3",
        "2 ** 8",
        "3 ^ 4",
        "-5 + -3",
        "0 * 100",
        "7.5 / 2.5",
    ]
    
    print("✅ Valid Expressions:")
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            formatted_result = calc.format_result(result)
            print(f"  {expr:<12} = {formatted_result}")
        except Exception as e:
            print(f"  {expr:<12} = ERROR: {e}")
    
    print("\n❌ Invalid Expressions (Error Handling):")
    invalid_expressions = [
        "5 / 0",         # Division by zero
        "5 +",           # Missing operand
        "abc + 3",       # Invalid number
        "5 & 3",         # Invalid operator
    ]
    
    for expr in invalid_expressions:
        try:
            result = calc.calculate(expr)
            print(f"  {expr:<12} = {result} (UNEXPECTED)")
        except Exception as e:
            print(f"  {expr:<12} = ERROR: {e}")
    
    print("\n✅ All manual tests completed!")


def main():
    """Main function to run all tests."""
    print("🧮 Python Calculator Test Suite")
    print("=" * 60)
    
    # Run unit tests
    print("\n🔬 Running Unit Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run manual tests
    print("\n" + "=" * 60)
    run_manual_tests()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("💡 To run the calculator: python calculator.py")


if __name__ == "__main__":
    main()
