#!/usr/bin/env python3
"""
Python Calculator Application
A command-line calculator with basic arithmetic operations and error handling.

Author: Jai Jaish
Version: 1.0.0
Python Version: 3.10+
"""

import re
import sys
from typing import Union, Tuple


class Calculator:
    """
    A comprehensive calculator class that handles basic arithmetic operations
    with proper error handling and input validation.
    """
    
    def __init__(self):
        """Initialize the calculator with supported operations."""
        self.operations = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
            '**': self.power,
            '^': self.power  # Alternative power operator
        }
        
        # Pattern to match valid mathematical expressions
        self.expression_pattern = re.compile(
            r'^(-?\d*\.?\d+)\s*([\+\-\*/\^]|\*\*)\s*(-?\d*\.?\d+)$'
        )
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract second number from first number."""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """
        Divide first number by second number.
        Raises ZeroDivisionError if divisor is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero!")
        return a / b
    
    def power(self, a: float, b: float) -> float:
        """Raise first number to the power of second number."""
        try:
            result = a ** b
            # Check for overflow
            if abs(result) > 1e308:
                raise OverflowError("Result is too large to display!")
            return result
        except OverflowError:
            raise OverflowError("Result is too large to display!")
    
    def parse_expression(self, expression: str) -> Tuple[float, str, float]:
        """
        Parse a mathematical expression into operands and operator.
        
        Args:
            expression (str): Mathematical expression like "5 + 3"
            
        Returns:
            Tuple[float, str, float]: (operand1, operator, operand2)
            
        Raises:
            ValueError: If expression format is invalid
        """
        # Remove extra whitespace
        expression = expression.strip()
        
        # Check if expression matches valid pattern
        match = self.expression_pattern.match(expression)
        if not match:
            raise ValueError("Invalid expression format! Use format: number operator number")
        
        # Extract components
        operand1_str, operator, operand2_str = match.groups()
        
        try:
            operand1 = float(operand1_str)
            operand2 = float(operand2_str)
        except ValueError:
            raise ValueError("Invalid number format in expression!")
        
        return operand1, operator, operand2
    
    def calculate(self, expression: str) -> Union[float, int]:
        """
        Calculate the result of a mathematical expression.
        
        Args:
            expression (str): Mathematical expression to evaluate
            
        Returns:
            Union[float, int]: Calculated result
            
        Raises:
            ValueError: For invalid expressions or unsupported operations
            ZeroDivisionError: For division by zero
            OverflowError: For results too large to display
        """
        # Parse the expression
        operand1, operator, operand2 = self.parse_expression(expression)
        
        # Check if operator is supported
        if operator not in self.operations:
            raise ValueError(f"Unsupported operation: {operator}")
        
        # Perform calculation
        result = self.operations[operator](operand1, operand2)
        
        # Return integer if result is a whole number
        if isinstance(result, float) and result.is_integer():
            return int(result)
        
        return result
    
    def format_result(self, result: Union[float, int]) -> str:
        """
        Format the result for display.
        
        Args:
            result (Union[float, int]): Calculation result
            
        Returns:
            str: Formatted result string
        """
        if isinstance(result, int):
            return str(result)
        elif isinstance(result, float):
            # Round to 10 decimal places to avoid floating point precision issues
            rounded_result = round(result, 10)
            if rounded_result.is_integer():
                return str(int(rounded_result))
            else:
                # Remove trailing zeros
                return f"{rounded_result:g}"
        else:
            return str(result)


def display_welcome_message():
    """Display welcome message and instructions."""
    print("=" * 60)
    print("🧮 PYTHON CALCULATOR")
    print("=" * 60)
    print("Welcome to the Python Calculator!")
    print("\nSupported Operations:")
    print("  Addition:       5 + 3")
    print("  Subtraction:    10 - 4")
    print("  Multiplication: 6 * 7")
    print("  Division:       15 / 3")
    print("  Exponentiation: 2 ** 3  or  2 ^ 3")
    print("\nFeatures:")
    print("  ✓ Supports decimal numbers (e.g., 3.14 + 2.86)")
    print("  ✓ Supports negative numbers (e.g., -5 + 3)")
    print("  ✓ Error handling for invalid inputs")
    print("  ✓ Division by zero protection")
    print("\nInstructions:")
    print("  • Enter expressions like: 5 + 3")
    print("  • Type 'quit', 'exit', or 'q' to exit")
    print("  • Type 'help' to see this message again")
    print("=" * 60)


def display_help():
    """Display help information."""
    print("\n" + "=" * 40)
    print("📚 HELP - Calculator Usage")
    print("=" * 40)
    print("Expression Format: number operator number")
    print("\nExamples:")
    print("  5 + 3        → Addition")
    print("  10.5 - 2.3   → Subtraction with decimals")
    print("  -4 * 6       → Multiplication with negative")
    print("  15 / 3       → Division")
    print("  2 ** 8       → Exponentiation (power)")
    print("  3 ^ 4        → Alternative power notation")
    print("\nSpecial Commands:")
    print("  help, h      → Show this help")
    print("  quit, exit, q → Exit calculator")
    print("=" * 40)


def get_user_input() -> str:
    """
    Get user input with proper prompting.
    
    Returns:
        str: User input string
    """
    try:
        return input("\n🧮 Enter calculation (or 'help'/'quit'): ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye! Thanks for using Python Calculator!")
        sys.exit(0)


def main():
    """
    Main function to run the calculator application.
    Handles the main program loop and user interactions.
    """
    # Initialize calculator
    calc = Calculator()
    
    # Display welcome message
    display_welcome_message()
    
    # Main program loop
    while True:
        try:
            # Get user input
            user_input = get_user_input()
            
            # Handle empty input
            if not user_input:
                print("⚠️  Please enter a calculation or 'quit' to exit.")
                continue
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye! Thanks for using Python Calculator!")
                break
            
            elif user_input.lower() in ['help', 'h']:
                display_help()
                continue
            
            # Perform calculation
            try:
                result = calc.calculate(user_input)
                formatted_result = calc.format_result(result)
                
                print(f"📊 Result: {user_input} = {formatted_result}")
                
            except ValueError as e:
                print(f"❌ Error: {e}")
                print("💡 Tip: Use format 'number operator number' (e.g., 5 + 3)")
                
            except ZeroDivisionError as e:
                print(f"❌ Math Error: {e}")
                print("💡 Tip: Division by zero is undefined in mathematics")
                
            except OverflowError as e:
                print(f"❌ Overflow Error: {e}")
                print("💡 Tip: Try smaller numbers")
                
            except Exception as e:
                print(f"❌ Unexpected Error: {e}")
                print("💡 Tip: Please check your input format")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Python Calculator!")
            break
        
        except Exception as e:
            print(f"❌ System Error: {e}")
            print("💡 Please try again or type 'quit' to exit")


if __name__ == "__main__":
    main()
