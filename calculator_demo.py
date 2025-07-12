#!/usr/bin/env python3
"""
Demo script for the Python Calculator Application
Demonstrates all features and capabilities of the calculator.
"""

from calculator import Calculator
import time


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*50}")
    print(f"🧮 {title}")
    print('='*50)


def demo_calculation(calc, expression, description=""):
    """Demonstrate a single calculation with formatting."""
    try:
        result = calc.calculate(expression)
        formatted_result = calc.format_result(result)
        desc_text = f" ({description})" if description else ""
        print(f"  {expression:<15} = {formatted_result:<15}{desc_text}")
        return True
    except Exception as e:
        print(f"  {expression:<15} = ERROR: {e}")
        return False


def main():
    """Main demo function."""
    print("🎯 Python Calculator - Feature Demonstration")
    print("=" * 60)
    print("This demo showcases all the features of our calculator!")
    
    # Initialize calculator
    calc = Calculator()
    
    # Basic Operations Demo
    print_section("BASIC ARITHMETIC OPERATIONS")
    demo_calculation(calc, "5 + 3", "Addition")
    demo_calculation(calc, "10 - 4", "Subtraction")
    demo_calculation(calc, "6 * 7", "Multiplication")
    demo_calculation(calc, "15 / 3", "Division")
    demo_calculation(calc, "2 ** 3", "Exponentiation")
    demo_calculation(calc, "3 ^ 4", "Alternative power notation")
    
    # Decimal Numbers Demo
    print_section("DECIMAL NUMBER SUPPORT")
    demo_calculation(calc, "3.14 + 2.86", "Pi + e approximation")
    demo_calculation(calc, "10.5 - 2.3", "Decimal subtraction")
    demo_calculation(calc, "2.5 * 4.2", "Decimal multiplication")
    demo_calculation(calc, "7.5 / 2.5", "Decimal division")
    demo_calculation(calc, "1.5 ** 2", "Decimal exponentiation")
    
    # Negative Numbers Demo
    print_section("NEGATIVE NUMBER HANDLING")
    demo_calculation(calc, "-5 + 3", "Negative + positive")
    demo_calculation(calc, "5 + -3", "Positive + negative")
    demo_calculation(calc, "-5 + -3", "Negative + negative")
    demo_calculation(calc, "-10 - -5", "Double negative")
    demo_calculation(calc, "-4 * -3", "Negative multiplication")
    demo_calculation(calc, "-15 / -3", "Negative division")
    demo_calculation(calc, "-2 ** 3", "Negative exponentiation")
    
    # Edge Cases Demo
    print_section("EDGE CASES & SPECIAL VALUES")
    demo_calculation(calc, "0 + 0", "Zero addition")
    demo_calculation(calc, "0 * 100", "Zero multiplication")
    demo_calculation(calc, "0 / 5", "Zero division")
    demo_calculation(calc, "5 ** 0", "Power of zero")
    demo_calculation(calc, "1 ** 100", "One to any power")
    demo_calculation(calc, "4 ** 0.5", "Square root via power")
    
    # Large Numbers Demo
    print_section("LARGE NUMBER CALCULATIONS")
    demo_calculation(calc, "1000000 + 2000000", "Million-scale addition")
    demo_calculation(calc, "1000 * 1000", "Thousand squared")
    demo_calculation(calc, "2 ** 10", "2 to the 10th power")
    demo_calculation(calc, "10 ** 6", "Scientific notation equivalent")
    
    # Small Numbers Demo
    print_section("SMALL NUMBER PRECISION")
    demo_calculation(calc, "0.1 + 0.2", "Floating point precision")
    demo_calculation(calc, "0.0001 + 0.0002", "Very small numbers")
    demo_calculation(calc, "0.1 * 0.1", "Small multiplication")
    demo_calculation(calc, "1 / 3", "Repeating decimal")
    
    # Error Handling Demo
    print_section("ERROR HANDLING DEMONSTRATION")
    print("The calculator gracefully handles various error conditions:")
    demo_calculation(calc, "5 / 0", "Division by zero")
    demo_calculation(calc, "10 / 0", "Another division by zero")
    
    # Invalid expressions (these will show errors)
    print("\nInvalid expression handling:")
    invalid_expressions = [
        ("5 +", "Missing operand"),
        ("+ 3", "Missing first operand"),
        ("5 & 3", "Invalid operator"),
        ("abc + 3", "Invalid number"),
        ("5 + def", "Invalid second number"),
    ]
    
    for expr, desc in invalid_expressions:
        demo_calculation(calc, expr, desc)
    
    # Performance Demo
    print_section("PERFORMANCE & FORMATTING")
    print("Result formatting examples:")
    
    test_cases = [
        ("10 / 2", "Integer result from division"),
        ("10 / 3", "Decimal result"),
        ("1000000 + 1", "Large integer"),
        ("0.000001 * 1000000", "Scientific precision"),
    ]
    
    for expr, desc in test_cases:
        demo_calculation(calc, expr, desc)
    
    # Summary
    print_section("SUMMARY")
    print("✅ Features Demonstrated:")
    print("  • Basic arithmetic operations (+, -, *, /, **)")
    print("  • Alternative power notation (^)")
    print("  • Decimal number support")
    print("  • Negative number handling")
    print("  • Error handling (division by zero, invalid input)")
    print("  • Input validation and parsing")
    print("  • Result formatting (integer/decimal)")
    print("  • Large and small number support")
    print("  • Floating point precision handling")
    
    print("\n🎯 Calculator Features:")
    print("  • Object-oriented design")
    print("  • Comprehensive error handling")
    print("  • Regular expression parsing")
    print("  • Type hints for better code quality")
    print("  • Extensive test coverage")
    print("  • User-friendly interface")
    
    print("\n🚀 Usage:")
    print("  python calculator.py    # Interactive mode")
    print("  python test_calculator.py    # Run tests")
    print("  python calculator_demo.py    # This demo")
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed! The calculator is ready for use.")
    print("=" * 60)


if __name__ == "__main__":
    main()
