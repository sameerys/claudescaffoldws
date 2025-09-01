#!/usr/bin/env python3
"""
Comprehensive Unit Tests for Fibonacci Program

This test suite covers all methods, edge cases, error handling,
performance considerations, and interactive interface functionality.

Test Categories:
- Basic functionality tests for all calculation methods
- Edge cases (0, 1, negative numbers, large numbers)
- Error handling and exception testing
- Performance and memoization testing
- Generator functionality
- Interactive interface simulation
- Benchmark functionality

Author: Generated for ScaffoldWS Project
Date: 2025-09-01
"""

import pytest
import time
import sys
from unittest.mock import patch, MagicMock
from io import StringIO
from typing import List, Iterator

# Import the modules under test
sys.path.insert(0, 'C:\\Sameer\\Projects\\CopilotAgent\\ScaffoldWS\\src')
from fibonacci import (
    FibonacciGenerator, 
    FibonacciError, 
    benchmark_methods, 
    interactive_interface,
    main
)


class TestFibonacciGenerator:
    """Test cases for the FibonacciGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.fib = FibonacciGenerator()
    
    def teardown_method(self):
        """Clean up after each test method."""
        self.fib.clear_cache()


class TestIterativeMethod(TestFibonacciGenerator):
    """Test cases for the iterative Fibonacci calculation method."""
    
    def test_iterative_base_cases(self):
        """Test iterative method with base cases F(0) and F(1)."""
        assert self.fib.iterative(0) == 0
        assert self.fib.iterative(1) == 1
    
    def test_iterative_small_numbers(self):
        """Test iterative method with small Fibonacci numbers."""
        expected_values = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
        for i, expected in enumerate(expected_values):
            assert self.fib.iterative(i) == expected, f"F({i}) should be {expected}"
    
    def test_iterative_larger_numbers(self):
        """Test iterative method with larger Fibonacci numbers."""
        # Test some known larger Fibonacci numbers
        assert self.fib.iterative(20) == 6765
        assert self.fib.iterative(30) == 832040
        assert self.fib.iterative(40) == 102334155
    
    def test_iterative_negative_input(self):
        """Test iterative method raises error for negative input."""
        with pytest.raises(FibonacciError, match="not defined for negative numbers"):
            self.fib.iterative(-1)
        
        with pytest.raises(FibonacciError, match="not defined for negative numbers"):
            self.fib.iterative(-10)
    
    def test_iterative_performance(self):
        """Test that iterative method performs efficiently for large numbers."""
        start_time = time.perf_counter()
        result = self.fib.iterative(1000)
        end_time = time.perf_counter()
        
        # Should complete very quickly (under 1 second)
        assert end_time - start_time < 1.0
        assert isinstance(result, int)
        assert result > 0


class TestRecursiveMethod(TestFibonacciGenerator):
    """Test cases for the recursive Fibonacci calculation method."""
    
    def test_recursive_base_cases(self):
        """Test recursive method with base cases F(0) and F(1)."""
        assert self.fib.recursive(0) == 0
        assert self.fib.recursive(1) == 1
    
    def test_recursive_small_numbers(self):
        """Test recursive method with small Fibonacci numbers."""
        expected_values = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        for i, expected in enumerate(expected_values):
            assert self.fib.recursive(i) == expected, f"F({i}) should be {expected}"
    
    def test_recursive_moderate_numbers(self):
        """Test recursive method with moderate numbers (up to 25)."""
        # Test up to F(25) as recursive method is slow
        assert self.fib.recursive(15) == 610
        assert self.fib.recursive(20) == 6765
        assert self.fib.recursive(25) == 75025
    
    def test_recursive_negative_input(self):
        """Test recursive method raises error for negative input."""
        with pytest.raises(FibonacciError, match="not defined for negative numbers"):
            self.fib.recursive(-1)
        
        with pytest.raises(FibonacciError, match="not defined for negative numbers"):
            self.fib.recursive(-5)
    
    def test_recursive_consistency_with_iterative(self):
        """Test that recursive method gives same results as iterative for small n."""
        for n in range(20):  # Test up to 20 to avoid performance issues
            assert self.fib.recursive(n) == self.fib.iterative(n), \
                f"Recursive and iterative should match for F({n})"


class TestMemoizedRecursiveMethod(TestFibonacciGenerator):
    """Test cases for the memoized recursive Fibonacci calculation method."""
    
    def test_memoized_base_cases(self):
        """Test memoized method with base cases F(0) and F(1)."""
        assert self.fib.memoized_recursive(0) == 0
        assert self.fib.memoized_recursive(1) == 1
    
    def test_memoized_small_numbers(self):
        """Test memoized method with small Fibonacci numbers."""
        expected_values = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
        for i, expected in enumerate(expected_values):
            assert self.fib.memoized_recursive(i) == expected, f"F({i}) should be {expected}"
    
    def test_memoized_large_numbers(self):
        """Test memoized method with large Fibonacci numbers."""
        assert self.fib.memoized_recursive(50) == 12586269025
        assert self.fib.memoized_recursive(100) == 354224848179261915075
    
    def test_memoized_negative_input(self):
        """Test memoized method raises error for negative input."""
        with pytest.raises(FibonacciError, match="not defined for negative numbers"):
            self.fib.memoized_recursive(-1)
    
    def test_memoized_cache_functionality(self):
        """Test that memoization cache works correctly."""
        # Clear cache and check initial state
        self.fib.clear_cache()
        assert len(self.fib._memo_cache) == 2  # Should have F(0) and F(1)
        
        # Calculate F(10) and verify cache growth
        result = self.fib.memoized_recursive(10)
        assert result == 55
        assert len(self.fib._memo_cache) >= 10  # Cache should contain intermediate values
        
        # Verify cached values are correct
        for i in range(11):
            assert i in self.fib._memo_cache
            assert self.fib._memo_cache[i] == self.fib.iterative(i)
    
    def test_memoized_performance_advantage(self):
        """Test that memoized method is faster than recursive for repeated calls."""
        n = 30
        
        # Time memoized method (first call)
        start_time = time.perf_counter()
        result1 = self.fib.memoized_recursive(n)
        end_time = time.perf_counter()
        first_call_time = end_time - start_time
        
        # Time memoized method (second call, should be cached)
        start_time = time.perf_counter()
        result2 = self.fib.memoized_recursive(n)
        end_time = time.perf_counter()
        second_call_time = end_time - start_time
        
        assert result1 == result2
        assert second_call_time < first_call_time  # Second call should be much faster
        assert second_call_time < 0.001  # Should be nearly instantaneous
    
    def test_clear_cache(self):
        """Test cache clearing functionality."""
        # Calculate some values to populate cache
        self.fib.memoized_recursive(20)
        assert len(self.fib._memo_cache) > 2
        
        # Clear cache and verify
        self.fib.clear_cache()
        assert len(self.fib._memo_cache) == 2
        assert self.fib._memo_cache == {0: 0, 1: 1}


class TestSequenceGenerator(TestFibonacciGenerator):
    """Test cases for the sequence generator method."""
    
    def test_generator_basic_functionality(self):
        """Test generator produces correct Fibonacci sequence."""
        gen = self.fib.sequence_generator(10)
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        result = list(gen)
        assert result == expected
    
    def test_generator_unlimited(self):
        """Test generator without limit (take first few values)."""
        gen = self.fib.sequence_generator()
        first_ten = []
        for i, value in enumerate(gen):
            if i >= 10:
                break
            first_ten.append(value)
        
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        assert first_ten == expected
    
    def test_generator_single_value(self):
        """Test generator with max_count=1."""
        gen = self.fib.sequence_generator(1)
        result = list(gen)
        assert result == [0]
    
    def test_generator_zero_count(self):
        """Test generator with max_count=0."""
        gen = self.fib.sequence_generator(0)
        result = list(gen)
        assert result == []
    
    def test_generator_negative_count(self):
        """Test generator raises error for negative max_count."""
        with pytest.raises(FibonacciError, match="Maximum count cannot be negative"):
            list(self.fib.sequence_generator(-1))
    
    def test_generator_is_iterator(self):
        """Test that generator returns an iterator."""
        gen = self.fib.sequence_generator(5)
        assert hasattr(gen, '__iter__')
        assert hasattr(gen, '__next__')
    
    def test_generator_memory_efficiency(self):
        """Test generator doesn't consume excessive memory for large sequences."""
        gen = self.fib.sequence_generator(1000)
        
        # Should be able to create generator without computing all values
        assert gen is not None
        
        # Take just a few values to verify it works
        first_five = []
        for i, value in enumerate(gen):
            if i >= 5:
                break
            first_five.append(value)
        
        assert first_five == [0, 1, 1, 2, 3]


class TestGetSequenceMethod(TestFibonacciGenerator):
    """Test cases for the get_sequence method."""
    
    def test_get_sequence_default_method(self):
        """Test get_sequence with default iterative method."""
        result = self.fib.get_sequence(10)
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        assert result == expected
    
    def test_get_sequence_iterative_method(self):
        """Test get_sequence with explicit iterative method."""
        result = self.fib.get_sequence(8, 'iterative')
        expected = [0, 1, 1, 2, 3, 5, 8, 13]
        assert result == expected
    
    def test_get_sequence_recursive_method(self):
        """Test get_sequence with recursive method."""
        result = self.fib.get_sequence(6, 'recursive')
        expected = [0, 1, 1, 2, 3, 5]
        assert result == expected
    
    def test_get_sequence_memoized_method(self):
        """Test get_sequence with memoized method."""
        result = self.fib.get_sequence(10, 'memoized')
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        assert result == expected
    
    def test_get_sequence_generator_method(self):
        """Test get_sequence with generator method."""
        result = self.fib.get_sequence(10, 'generator')
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        assert result == expected
    
    def test_get_sequence_case_insensitive(self):
        """Test get_sequence method names are case insensitive."""
        result1 = self.fib.get_sequence(5, 'ITERATIVE')
        result2 = self.fib.get_sequence(5, 'Iterative')
        result3 = self.fib.get_sequence(5, 'iterative')
        
        expected = [0, 1, 1, 2, 3]
        assert result1 == result2 == result3 == expected
    
    def test_get_sequence_zero_count(self):
        """Test get_sequence with n=0."""
        for method in ['iterative', 'recursive', 'memoized', 'generator']:
            result = self.fib.get_sequence(0, method)
            assert result == []
    
    def test_get_sequence_negative_count(self):
        """Test get_sequence raises error for negative n."""
        with pytest.raises(FibonacciError, match="Number of terms cannot be negative"):
            self.fib.get_sequence(-1)
    
    def test_get_sequence_invalid_method(self):
        """Test get_sequence raises error for invalid method."""
        with pytest.raises(FibonacciError, match="Invalid method"):
            self.fib.get_sequence(5, 'invalid_method')
    
    def test_get_sequence_recursive_limit(self):
        """Test get_sequence prevents recursive method for large n."""
        with pytest.raises(FibonacciError, match="Recursive method is too slow"):
            self.fib.get_sequence(40, 'recursive')
    
    def test_get_sequence_method_consistency(self):
        """Test all methods produce the same sequence for small n."""
        n = 15
        iterative_result = self.fib.get_sequence(n, 'iterative')
        recursive_result = self.fib.get_sequence(n, 'recursive')
        memoized_result = self.fib.get_sequence(n, 'memoized')
        generator_result = self.fib.get_sequence(n, 'generator')
        
        assert iterative_result == recursive_result
        assert iterative_result == memoized_result
        assert iterative_result == generator_result


class TestFibonacciError:
    """Test cases for FibonacciError exception handling."""
    
    def test_fibonacci_error_is_exception(self):
        """Test FibonacciError is proper exception class."""
        error = FibonacciError("test message")
        assert isinstance(error, Exception)
        assert str(error) == "test message"
    
    def test_fibonacci_error_inheritance(self):
        """Test FibonacciError inherits from Exception."""
        assert issubclass(FibonacciError, Exception)


class TestBenchmarkMethods:
    """Test cases for the benchmark_methods function."""
    
    def test_benchmark_small_number(self):
        """Test benchmark with small number that allows all methods."""
        results = benchmark_methods(20)
        
        # Should have results for all methods
        expected_methods = ['iterative', 'memoized_recursive', 'recursive']
        for method in expected_methods:
            assert method in results
            assert isinstance(results[method], float)
            assert results[method] >= 0
    
    def test_benchmark_large_number(self):
        """Test benchmark with large number that excludes recursive method."""
        results = benchmark_methods(40)
        
        # Should have results for efficient methods only
        assert 'iterative' in results
        assert 'memoized_recursive' in results
        assert 'recursive' not in results
        
        # Results should be numeric (execution times)
        assert isinstance(results['iterative'], float)
        assert isinstance(results['memoized_recursive'], float)
    
    def test_benchmark_negative_number(self):
        """Test benchmark handles negative numbers gracefully."""
        results = benchmark_methods(-5)
        
        # Should have error results for all methods
        for method_name, result in results.items():
            if isinstance(result, str):
                assert "Error:" in result
            # If not an error string, then the method handled it and returned time
    
    def test_benchmark_zero(self):
        """Test benchmark with n=0."""
        results = benchmark_methods(0)
        
        # Should work fine with all methods
        for method_name, result in results.items():
            assert isinstance(result, float)
            assert result >= 0
    
    def test_benchmark_performance_comparison(self):
        """Test benchmark shows expected performance relationships."""
        results = benchmark_methods(30)
        
        # Iterative should be fastest for reasonable sizes
        assert isinstance(results['iterative'], float)
        assert isinstance(results['memoized_recursive'], float)
        
        # Both should complete reasonably quickly
        assert results['iterative'] < 1.0
        assert results['memoized_recursive'] < 1.0


class TestInteractiveInterface:
    """Test cases for the interactive interface functionality."""
    
    def test_interactive_interface_quit_command(self):
        """Test interactive interface handles quit command."""
        with patch('builtins.input', side_effect=['quit']):
            with patch('builtins.print') as mock_print:
                interactive_interface()
                
                # Should print goodbye message
                mock_print.assert_any_call("Thank you for using Fibonacci Generator! 👋")
    
    def test_interactive_interface_help_command(self):
        """Test interactive interface handles help command."""
        with patch('builtins.input', side_effect=['help', 'quit']):
            with patch('builtins.print') as mock_print:
                interactive_interface()
                
                # Should print help information
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'Command usage:' in printed_text
    
    def test_interactive_interface_single_command(self):
        """Test interactive interface handles single command."""
        with patch('builtins.input', side_effect=['single 10', 'quit']):
            with patch('builtins.print') as mock_print:
                interactive_interface()
                
                # Should calculate and display F(10) = 55
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert '55' in printed_text
    
    def test_interactive_interface_sequence_command(self):
        """Test interactive interface handles sequence command."""
        with patch('builtins.input', side_effect=['sequence 5', 'quit']):
            with patch('builtins.print') as mock_print:
                interactive_interface()
                
                # Should display first 5 Fibonacci numbers
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'First 5 Fibonacci numbers' in printed_text
    
    def test_interactive_interface_generator_command(self):
        """Test interactive interface handles generator command."""
        with patch('builtins.input', side_effect=['generator 5', 'quit']):
            with patch('builtins.print') as mock_print:
                interactive_interface()
                
                # Should use generator to display numbers
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'using generator' in printed_text
    
    def test_interactive_interface_benchmark_command(self):
        """Test interactive interface handles benchmark command."""
        with patch('builtins.input', side_effect=['benchmark 25', 'quit']):
            with patch('builtins.print') as mock_print:
                interactive_interface()
                
                # Should show benchmark results
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'Benchmarking methods' in printed_text
    
    def test_interactive_interface_invalid_command(self):
        """Test interactive interface handles invalid commands."""
        with patch('builtins.input', side_effect=['invalid_command', 'quit']):
            with patch('builtins.print') as mock_print:
                interactive_interface()
                
                # Should show error message
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'Unknown command' in printed_text
    
    def test_interactive_interface_empty_input(self):
        """Test interactive interface handles empty input gracefully."""
        with patch('builtins.input', side_effect=['', '   ', 'quit']):
            with patch('builtins.print'):
                # Should not raise any exceptions
                interactive_interface()
    
    def test_interactive_interface_value_error(self):
        """Test interactive interface handles invalid numbers."""
        with patch('builtins.input', side_effect=['single abc', 'quit']):
            with patch('builtins.print') as mock_print:
                interactive_interface()
                
                # Should show invalid input message
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'Invalid input' in printed_text
    
    def test_interactive_interface_fibonacci_error(self):
        """Test interactive interface handles FibonacciError."""
        with patch('builtins.input', side_effect=['single -5', 'quit']):
            with patch('builtins.print') as mock_print:
                interactive_interface()
                
                # Should show Fibonacci error message
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'Fibonacci Error' in printed_text
    
    def test_interactive_interface_keyboard_interrupt(self):
        """Test interactive interface handles keyboard interrupt."""
        with patch('builtins.input', side_effect=KeyboardInterrupt()):
            with patch('builtins.print') as mock_print:
                interactive_interface()
                
                # Should show interrupted message
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'interrupted by user' in printed_text


class TestMainFunction:
    """Test cases for the main function."""
    
    def test_main_no_arguments(self):
        """Test main function with no command line arguments."""
        with patch('sys.argv', ['fibonacci.py']):
            with patch('fibonacci.interactive_interface') as mock_interactive:
                main()
                mock_interactive.assert_called_once()
    
    def test_main_help_argument(self):
        """Test main function with help argument."""
        with patch('sys.argv', ['fibonacci.py', '--help']):
            with patch('builtins.print') as mock_print:
                main()
                
                # Should print help information
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'Usage:' in printed_text
    
    def test_main_single_number(self):
        """Test main function with single number argument."""
        with patch('sys.argv', ['fibonacci.py', '10']):
            with patch('builtins.print') as mock_print:
                main()
                
                # Should calculate and print F(10)
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert '55' in printed_text  # F(10) = 55
    
    def test_main_with_method(self):
        """Test main function with number and method arguments."""
        with patch('sys.argv', ['fibonacci.py', '8', 'memoized_recursive']):
            with patch('builtins.print') as mock_print:
                main()
                
                # Should calculate F(8) using memoized method
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert '21' in printed_text  # F(8) = 21
                assert 'memoized_recursive' in printed_text
    
    def test_main_sequence_mode(self):
        """Test main function with sequence mode."""
        with patch('sys.argv', ['fibonacci.py', '5', 'sequence']):
            with patch('builtins.print') as mock_print:
                main()
                
                # Should print sequence
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'First 5 Fibonacci numbers' in printed_text
    
    def test_main_invalid_number(self):
        """Test main function with invalid number argument."""
        with patch('sys.argv', ['fibonacci.py', 'abc']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit):
                    main()
                
                # Should show error message
                mock_print.assert_called_with("Error: Please provide a valid integer")
    
    def test_main_invalid_method(self):
        """Test main function with invalid method argument."""
        with patch('sys.argv', ['fibonacci.py', '10', 'invalid_method']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit):
                    main()
                
                # Should show error about invalid method
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'Invalid method' in printed_text
    
    def test_main_fibonacci_error(self):
        """Test main function handles FibonacciError."""
        with patch('sys.argv', ['fibonacci.py', '-5']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit):
                    main()
                
                # Should show Fibonacci error
                printed_text = ''.join(str(call) for call in mock_print.call_args_list)
                assert 'Error:' in printed_text


class TestEdgeCasesAndBoundaryConditions:
    """Test edge cases and boundary conditions across all methods."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fib = FibonacciGenerator()
    
    def test_very_large_numbers(self):
        """Test handling of very large Fibonacci numbers."""
        # Test iterative and memoized methods with large numbers
        n = 500
        result_iterative = self.fib.iterative(n)
        result_memoized = self.fib.memoized_recursive(n)
        
        # Results should be identical and very large integers
        assert result_iterative == result_memoized
        assert isinstance(result_iterative, int)
        assert result_iterative > 10**100  # F(500) is enormous
    
    def test_method_consistency_comprehensive(self):
        """Comprehensive test that all methods produce identical results."""
        test_values = [0, 1, 2, 3, 5, 8, 10, 15, 20, 25, 30]
        
        for n in test_values:
            iterative_result = self.fib.iterative(n)
            memoized_result = self.fib.memoized_recursive(n)
            
            # Clear cache for fair comparison
            self.fib.clear_cache()
            
            if n <= 30:  # Only test recursive for reasonable values
                recursive_result = self.fib.recursive(n)
                assert iterative_result == recursive_result, f"Methods differ at F({n})"
            
            assert iterative_result == memoized_result, f"Methods differ at F({n})"
            
            # Test generator produces same individual values
            gen_sequence = list(self.fib.sequence_generator(n + 1))
            assert gen_sequence[n] == iterative_result, f"Generator differs at F({n})"
    
    def test_memory_usage_patterns(self):
        """Test memory usage patterns for different methods."""
        # This is a behavioral test - methods should not consume excessive memory
        n = 100
        
        # Generator should not store all values
        gen = self.fib.sequence_generator(n)
        first_val = next(gen)
        assert first_val == 0  # Should work without computing all values
        
        # Memoized method should cache efficiently
        self.fib.clear_cache()
        self.fib.memoized_recursive(50)
        cache_size = len(self.fib._memo_cache)
        assert cache_size == 51  # Should cache F(0) through F(50)
    
    def test_type_safety(self):
        """Test that all methods return proper integer types."""
        test_values = [0, 1, 10, 50]
        
        for n in test_values:
            assert isinstance(self.fib.iterative(n), int)
            assert isinstance(self.fib.memoized_recursive(n), int)
            if n <= 30:
                assert isinstance(self.fib.recursive(n), int)
        
        # Generator should yield integers
        for value in self.fib.sequence_generator(5):
            assert isinstance(value, int)
    
    def test_sequence_boundaries(self):
        """Test sequence generation at boundary conditions."""
        # Empty sequence
        assert self.fib.get_sequence(0) == []
        
        # Single element sequences
        assert self.fib.get_sequence(1) == [0]
        
        # Two element sequence
        assert self.fib.get_sequence(2) == [0, 1]
        
        # Verify boundary behavior for all methods
        for method in ['iterative', 'recursive', 'memoized', 'generator']:
            if method == 'recursive':
                continue  # Skip recursive for this comprehensive test
            
            result = self.fib.get_sequence(3, method)
            assert result == [0, 1, 1], f"Boundary test failed for {method}"


class TestPerformanceCharacteristics:
    """Test performance characteristics and behavior under load."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fib = FibonacciGenerator()
    
    def test_iterative_linear_performance(self):
        """Test that iterative method has roughly linear time complexity."""
        # Test with increasing values
        times = []
        values = [100, 200, 300, 400, 500]
        
        for n in values:
            start_time = time.perf_counter()
            self.fib.iterative(n)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        # All should be reasonably fast (under 0.1 seconds)
        for t in times:
            assert t < 0.1, "Iterative method should be fast for reasonable inputs"
    
    def test_memoization_effectiveness(self):
        """Test that memoization provides expected performance benefits."""
        n = 100
        
        # First calculation (builds cache)
        start_time = time.perf_counter()
        result1 = self.fib.memoized_recursive(n)
        end_time = time.perf_counter()
        first_time = end_time - start_time
        
        # Second calculation (uses cache)
        start_time = time.perf_counter()
        result2 = self.fib.memoized_recursive(n)
        end_time = time.perf_counter()
        second_time = end_time - start_time
        
        assert result1 == result2
        assert second_time < first_time * 0.1  # Should be at least 10x faster
        assert second_time < 0.001  # Should be nearly instantaneous
    
    def test_generator_memory_efficiency(self):
        """Test that generator doesn't precompute values."""
        # Create generator for large sequence
        gen = self.fib.sequence_generator(10000)
        
        # Should create instantly without computing values
        start_time = time.perf_counter()
        first_value = next(gen)
        end_time = time.perf_counter()
        
        assert first_value == 0
        assert end_time - start_time < 0.001  # Should be nearly instant
        
        # Should be able to get subsequent values without issue
        second_value = next(gen)
        third_value = next(gen)
        
        assert second_value == 1
        assert third_value == 1


if __name__ == "__main__":
    # Configuration for running tests
    print("Running Fibonacci Unit Tests...")
    print("=" * 60)
    
    # Run the tests with verbose output
    pytest.main([
        __file__,
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--durations=10",  # Show 10 slowest tests
        "-x",  # Stop on first failure (optional)
    ])