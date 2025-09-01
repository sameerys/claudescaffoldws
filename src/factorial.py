#!/usr/bin/env python3
"""
Factorial Calculator Program

This module provides functions to calculate factorial of a number using
both iterative and recursive approaches, along with input validation
and error handling.

Author: Generated with Claude Code
"""

import sys
from typing import Union


def factorial_iterative(n: int) -> int:
    """
    Calculate factorial using iterative approach.
    
    Args:
        n (int): Non-negative integer to calculate factorial for
        
    Returns:
        int: Factorial of n
        
    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    if n <= 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


def factorial_recursive(n: int) -> int:
    """
    Calculate factorial using recursive approach.
    
    Args:
        n (int): Non-negative integer to calculate factorial for
        
    Returns:
        int: Factorial of n
        
    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
        RecursionError: If n is too large causing stack overflow
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    if n <= 1:
        return 1
    
    return n * factorial_recursive(n - 1)


def get_user_input() -> int:
    """
    Get and validate user input for factorial calculation.
    
    Returns:
        int: Valid non-negative integer from user
    """
    while True:
        try:
            user_input = input("Enter a non-negative integer to calculate its factorial (or 'q' to quit): ").strip()
            
            if user_input.lower() == 'q':
                print("Goodbye!")
                sys.exit(0)
            
            number = int(user_input)
            
            if number < 0:
                print("Error: Please enter a non-negative integer.")
                continue
                
            return number
            
        except ValueError:
            print("Error: Please enter a valid integer or 'q' to quit.")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Goodbye!")
            sys.exit(0)


def display_result(n: int, iterative_result: int, recursive_result: int) -> None:
    """
    Display the factorial results in a formatted manner.
    
    Args:
        n (int): The input number
        iterative_result (int): Result from iterative calculation
        recursive_result (int): Result from recursive calculation
    """
    print(f"\nResults for {n}!")
    print(f"Iterative approach: {iterative_result:,}")
    print(f"Recursive approach: {recursive_result:,}")
    print("-" * 50)


def main() -> None:
    """
    Main function to run the factorial calculator program.
    """
    print("=== Factorial Calculator ===")
    print("This program calculates factorial using both iterative and recursive methods.")
    print("Note: Large numbers may cause recursion limits or long computation times.")
    print()
    
    while True:
        try:
            number = get_user_input()
            
            # Calculate using both methods
            iterative_result = factorial_iterative(number)
            
            # For very large numbers, recursive might hit recursion limit
            try:
                recursive_result = factorial_recursive(number)
            except RecursionError:
                recursive_result = "RecursionError (number too large)"
                print(f"\nResults for {number}!")
                print(f"Iterative approach: {iterative_result:,}")
                print(f"Recursive approach: {recursive_result}")
                print("-" * 50)
                continue
            
            display_result(number, iterative_result, recursive_result)
            
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()