#!/usr/bin/env python3
"""
Fibonacci Sequence Generator

This module provides multiple implementations for generating Fibonacci sequences:
- Iterative approach (most efficient)
- Recursive approach (demonstrates recursion)
- Generator approach (memory efficient for large sequences)
- Memoized recursive approach (optimized recursion)

The Fibonacci sequence is defined as:
F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n > 1

Author: Generated for ScaffoldWS Project
Date: 2025-09-01
"""

import time
import sys
from typing import Iterator, List, Dict


class FibonacciError(Exception):
    """Custom exception for Fibonacci-related errors."""
    pass


class FibonacciGenerator:
    """A comprehensive Fibonacci sequence generator with multiple implementations."""
    
    def __init__(self):
        """Initialize the Fibonacci generator with memoization cache."""
        self._memo_cache: Dict[int, int] = {0: 0, 1: 1}
    
    def iterative(self, n: int) -> int:
        """
        Calculate the nth Fibonacci number using iterative approach.
        
        Args:
            n (int): Position in the Fibonacci sequence (0-indexed)
            
        Returns:
            int: The nth Fibonacci number
            
        Raises:
            FibonacciError: If n is negative
            
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if n < 0:
            raise FibonacciError("Fibonacci sequence is not defined for negative numbers")
        
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        
        return b
    
    def recursive(self, n: int) -> int:
        """
        Calculate the nth Fibonacci number using naive recursive approach.
        
        Args:
            n (int): Position in the Fibonacci sequence (0-indexed)
            
        Returns:
            int: The nth Fibonacci number
            
        Raises:
            FibonacciError: If n is negative
            
        Time Complexity: O(2^n) - exponential, very slow for large n
        Space Complexity: O(n) - due to recursion stack
        
        Note: This implementation is inefficient and should not be used for n > 35
        """
        if n < 0:
            raise FibonacciError("Fibonacci sequence is not defined for negative numbers")
        
        if n <= 1:
            return n
        
        return self.recursive(n - 1) + self.recursive(n - 2)
    
    def memoized_recursive(self, n: int) -> int:
        """
        Calculate the nth Fibonacci number using memoized recursive approach.
        
        Args:
            n (int): Position in the Fibonacci sequence (0-indexed)
            
        Returns:
            int: The nth Fibonacci number
            
        Raises:
            FibonacciError: If n is negative
            
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        if n < 0:
            raise FibonacciError("Fibonacci sequence is not defined for negative numbers")
        
        if n in self._memo_cache:
            return self._memo_cache[n]
        
        self._memo_cache[n] = (self.memoized_recursive(n - 1) + 
                               self.memoized_recursive(n - 2))
        return self._memo_cache[n]
    
    def sequence_generator(self, max_count: int = None) -> Iterator[int]:
        """
        Generate Fibonacci sequence using a generator (memory efficient).
        
        Args:
            max_count (int, optional): Maximum number of terms to generate.
                                     If None, generates indefinitely.
            
        Yields:
            int: Next Fibonacci number in sequence
            
        Raises:
            FibonacciError: If max_count is negative
        """
        if max_count is not None and max_count < 0:
            raise FibonacciError("Maximum count cannot be negative")
        
        a, b = 0, 1
        count = 0
        
        while max_count is None or count < max_count:
            yield a
            a, b = b, a + b
            count += 1
    
    def get_sequence(self, n: int, method: str = 'iterative') -> List[int]:
        """
        Generate a list of the first n Fibonacci numbers.
        
        Args:
            n (int): Number of Fibonacci numbers to generate
            method (str): Method to use ('iterative', 'recursive', 'memoized', 'generator')
            
        Returns:
            List[int]: List of the first n Fibonacci numbers
            
        Raises:
            FibonacciError: If n is negative or method is invalid
        """
        if n < 0:
            raise FibonacciError("Number of terms cannot be negative")
        
        if n == 0:
            return []
        
        method = method.lower()
        
        if method == 'generator':
            return list(self.sequence_generator(n))
        elif method in ['iterative', 'recursive', 'memoized']:
            sequence = []
            for i in range(n):
                if method == 'iterative':
                    sequence.append(self.iterative(i))
                elif method == 'recursive':
                    if i > 35:  # Prevent extremely slow computation
                        raise FibonacciError(
                            "Recursive method is too slow for n > 35. "
                            "Use 'iterative', 'memoized', or 'generator' instead."
                        )
                    sequence.append(self.recursive(i))
                elif method == 'memoized':
                    sequence.append(self.memoized_recursive(i))
            return sequence
        else:
            raise FibonacciError(
                f"Invalid method '{method}'. "
                "Use 'iterative', 'recursive', 'memoized', or 'generator'"
            )
    
    def clear_cache(self):
        """Clear the memoization cache."""
        self._memo_cache = {0: 0, 1: 1}


def benchmark_methods(n: int) -> Dict[str, float]:
    """
    Benchmark different Fibonacci calculation methods.
    
    Args:
        n (int): The Fibonacci number to calculate
        
    Returns:
        Dict[str, float]: Dictionary with method names and execution times
    """
    fib = FibonacciGenerator()
    results = {}
    
    methods = [
        ('iterative', fib.iterative),
        ('memoized_recursive', fib.memoized_recursive)
    ]
    
    # Only test recursive for small values
    if n <= 35:
        methods.append(('recursive', fib.recursive))
    
    for method_name, method_func in methods:
        fib.clear_cache()  # Clear cache for fair comparison
        start_time = time.perf_counter()
        try:
            method_func(n)
            end_time = time.perf_counter()
            results[method_name] = end_time - start_time
        except Exception as e:
            results[method_name] = f"Error: {e}"
    
    return results


def interactive_interface():
    """Interactive command-line interface for the Fibonacci generator."""
    fib = FibonacciGenerator()
    
    print("=" * 60)
    print("🔢 Fibonacci Sequence Generator")
    print("=" * 60)
    print("\nAvailable commands:")
    print("1. 'single <n>' - Calculate nth Fibonacci number")
    print("2. 'sequence <n> [method]' - Generate first n Fibonacci numbers")
    print("3. 'benchmark <n>' - Benchmark different methods")
    print("4. 'generator <n>' - Use generator to display sequence")
    print("5. 'help' - Show this help message")
    print("6. 'quit' - Exit the program")
    print("\nMethods: iterative (default), recursive, memoized, generator")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\nEnter command: ").strip()
            
            if not user_input:
                continue
                
            parts = user_input.lower().split()
            command = parts[0]
            
            if command == 'quit':
                print("Thank you for using Fibonacci Generator! 👋")
                break
                
            elif command == 'help':
                print("\nCommand usage:")
                print("• single 10          - Get 10th Fibonacci number")
                print("• sequence 15        - Get first 15 numbers (iterative)")
                print("• sequence 10 recursive - Get first 10 numbers (recursive)")
                print("• benchmark 30       - Compare methods for F(30)")
                print("• generator 20       - Show first 20 numbers using generator")
                
            elif command == 'single':
                if len(parts) < 2:
                    print("❌ Usage: single <n>")
                    continue
                    
                n = int(parts[1])
                start_time = time.perf_counter()
                result = fib.iterative(n)
                end_time = time.perf_counter()
                
                print(f"✅ F({n}) = {result:,}")
                print(f"⏱️  Calculated in {end_time - start_time:.6f} seconds")
                
            elif command == 'sequence':
                if len(parts) < 2:
                    print("❌ Usage: sequence <n> [method]")
                    continue
                    
                n = int(parts[1])
                method = parts[2] if len(parts) > 2 else 'iterative'
                
                start_time = time.perf_counter()
                sequence = fib.get_sequence(n, method)
                end_time = time.perf_counter()
                
                print(f"✅ First {n} Fibonacci numbers ({method} method):")
                
                # Display in rows of 10 for better readability
                for i in range(0, len(sequence), 10):
                    row = sequence[i:i+10]
                    formatted_row = [f"{num:>8,}" for num in row]
                    print("   " + " ".join(formatted_row))
                
                print(f"⏱️  Generated in {end_time - start_time:.6f} seconds")
                
            elif command == 'benchmark':
                if len(parts) < 2:
                    print("❌ Usage: benchmark <n>")
                    continue
                    
                n = int(parts[1])
                print(f"🏃 Benchmarking methods for F({n})...")
                
                results = benchmark_methods(n)
                
                print("\n📊 Results:")
                for method, time_taken in results.items():
                    if isinstance(time_taken, str):
                        print(f"   {method:20}: {time_taken}")
                    else:
                        print(f"   {method:20}: {time_taken:.6f} seconds")
                
            elif command == 'generator':
                if len(parts) < 2:
                    print("❌ Usage: generator <n>")
                    continue
                    
                n = int(parts[1])
                print(f"✅ First {n} Fibonacci numbers (using generator):")
                
                count = 0
                for fib_num in fib.sequence_generator(n):
                    print(f"{fib_num:>8,}", end=" ")
                    count += 1
                    if count % 10 == 0:
                        print()  # New line every 10 numbers
                
                if count % 10 != 0:
                    print()  # Final new line if needed
                    
            else:
                print(f"❌ Unknown command: {command}")
                print("💡 Type 'help' for available commands")
                
        except ValueError as e:
            print(f"❌ Invalid input: Please enter a valid number")
        except FibonacciError as e:
            print(f"❌ Fibonacci Error: {e}")
        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


def main():
    """Main function to run the Fibonacci generator."""
    if len(sys.argv) > 1:
        # Command line mode
        try:
            if sys.argv[1] == '--help' or sys.argv[1] == '-h':
                print(__doc__)
                print("\nUsage:")
                print("  python fibonacci.py                    # Interactive mode")
                print("  python fibonacci.py <n>               # Calculate F(n)")
                print("  python fibonacci.py <n> <method>      # Calculate F(n) using method")
                print("  python fibonacci.py --help            # Show this help")
                return
            
            n = int(sys.argv[1])
            method = sys.argv[2] if len(sys.argv) > 2 else 'iterative'
            
            fib = FibonacciGenerator()
            
            if method.lower() == 'sequence':
                # Generate sequence
                sequence = fib.get_sequence(n)
                print(f"First {n} Fibonacci numbers:")
                for i, num in enumerate(sequence):
                    print(f"F({i}) = {num}")
            else:
                # Calculate single number
                start_time = time.perf_counter()
                result = getattr(fib, method.lower())(n)
                end_time = time.perf_counter()
                
                print(f"F({n}) = {result:,}")
                print(f"Method: {method}")
                print(f"Time: {end_time - start_time:.6f} seconds")
                
        except ValueError:
            print("Error: Please provide a valid integer")
            sys.exit(1)
        except AttributeError:
            print(f"Error: Invalid method '{sys.argv[2]}'. Use: iterative, recursive, memoized")
            sys.exit(1)
        except FibonacciError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        interactive_interface()


if __name__ == "__main__":
    main()