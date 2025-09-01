#!/usr/bin/env python3
"""
Integration and Advanced Tests for Fibonacci Program

This test suite focuses on integration testing, advanced scenarios,
and comprehensive system behavior validation.

Test Categories:
- Integration tests between different components
- End-to-end workflow testing
- Stress testing and performance validation
- Real-world usage scenario testing
- Cross-method validation and consistency checks

Author: Generated for ScaffoldWS Project
Date: 2025-09-01
"""

import pytest
import time
import sys
import io
from unittest.mock import patch, MagicMock
from contextlib import redirect_stdout, redirect_stderr

# Import the modules under test
sys.path.insert(0, 'C:\\Sameer\\Projects\\CopilotAgent\\ScaffoldWS\\src')
from fibonacci import (
    FibonacciGenerator, 
    FibonacciError, 
    benchmark_methods, 
    interactive_interface,
    main
)


class TestEndToEndWorkflows:
    """Test complete workflows from input to output."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fib = FibonacciGenerator()
    
    def test_complete_calculation_workflow(self):
        """Test complete calculation workflow for various inputs."""
        test_cases = [
            (0, 0), (1, 1), (5, 5), (10, 55), (15, 610), (20, 6765)
        ]
        
        for n, expected in test_cases:
            # Test all methods produce same result
            iterative_result = self.fib.iterative(n)
            memoized_result = self.fib.memoized_recursive(n)
            
            assert iterative_result == expected, f"Iterative F({n}) = {iterative_result}, expected {expected}"
            assert memoized_result == expected, f"Memoized F({n}) = {memoized_result}, expected {expected}"
            
            # Clear cache for next iteration
            self.fib.clear_cache()
    
    def test_sequence_generation_workflow(self):
        """Test complete sequence generation workflow."""
        methods = ['iterative', 'memoized', 'generator']
        sequence_length = 20
        
        # Generate sequences using different methods
        sequences = {}
        for method in methods:
            sequences[method] = self.fib.get_sequence(sequence_length, method)
        
        # All sequences should be identical
        base_sequence = sequences['iterative']
        for method, sequence in sequences.items():
            assert sequence == base_sequence, f"Sequence mismatch for method {method}"
        
        # Verify sequence properties
        assert len(base_sequence) == sequence_length
        assert base_sequence[0] == 0
        assert base_sequence[1] == 1
        
        # Verify Fibonacci property: F(n) = F(n-1) + F(n-2)
        for i in range(2, len(base_sequence)):
            expected = base_sequence[i-1] + base_sequence[i-2]
            assert base_sequence[i] == expected, f"Fibonacci property violated at index {i}"
    
    def test_interactive_session_simulation(self):
        """Test simulation of complete interactive session."""
        commands = [
            'single 10',
            'sequence 5',
            'generator 8',
            'benchmark 25',
            'help',
            'quit'
        ]
        
        with patch('builtins.input', side_effect=commands):
            with patch('builtins.print') as mock_print:
                interactive_interface()
        
        # Verify various commands were processed
        all_output = ' '.join(str(call) for call in mock_print.call_args_list)
        
        assert '55' in all_output  # F(10) = 55
        assert 'First 5 Fibonacci' in all_output
        assert 'using generator' in all_output
        assert 'Benchmarking methods' in all_output
        assert 'Command usage' in all_output
        assert 'Thank you' in all_output
    
    def test_command_line_interface_workflow(self):
        """Test command-line interface with various argument combinations."""
        test_cases = [
            (['fibonacci.py', '10'], '55'),
            (['fibonacci.py', '5', 'iterative'], '5'),
            (['fibonacci.py', '8', 'memoized_recursive'], '21'),
            (['fibonacci.py', '5', 'sequence'], 'First 5 Fibonacci'),
        ]
        
        for args, expected_output in test_cases:
            with patch('sys.argv', args):
                with patch('builtins.print') as mock_print:
                    main()
                
                all_output = ' '.join(str(call) for call in mock_print.call_args_list)
                assert expected_output in all_output, f"Expected '{expected_output}' in output for args {args}"


class TestStressAndPerformance:
    """Stress testing and performance validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fib = FibonacciGenerator()
    
    @pytest.mark.slow
    def test_large_number_stress_test(self):
        """Stress test with very large Fibonacci numbers."""
        large_numbers = [100, 500, 1000, 1500]
        
        for n in large_numbers:
            # Test iterative method (should always work)
            start_time = time.perf_counter()
            result_iterative = self.fib.iterative(n)
            iterative_time = time.perf_counter() - start_time
            
            # Test memoized method
            self.fib.clear_cache()
            start_time = time.perf_counter()
            result_memoized = self.fib.memoized_recursive(n)
            memoized_time = time.perf_counter() - start_time
            
            # Verify results are identical
            assert result_iterative == result_memoized, f"Results differ for F({n})"
            
            # Verify performance is reasonable (should complete within reasonable time)
            assert iterative_time < 10.0, f"Iterative method too slow for F({n}): {iterative_time}s"
            assert memoized_time < 10.0, f"Memoized method too slow for F({n}): {memoized_time}s"
            
            # Verify results are very large integers
            assert isinstance(result_iterative, int)
            assert result_iterative > 0
    
    def test_repeated_calculations_performance(self):
        """Test performance of repeated calculations."""
        n = 50
        iterations = 100
        
        # Test iterative method performance
        start_time = time.perf_counter()
        for _ in range(iterations):
            self.fib.iterative(n)
        iterative_total_time = time.perf_counter() - start_time
        
        # Test memoized method performance (first call builds cache)
        self.fib.clear_cache()
        self.fib.memoized_recursive(n)  # Prime the cache
        
        start_time = time.perf_counter()
        for _ in range(iterations):
            self.fib.memoized_recursive(n)
        memoized_total_time = time.perf_counter() - start_time
        
        # Memoized should be much faster for repeated calls
        assert memoized_total_time < iterative_total_time * 0.5, \
            "Memoized method should be faster for repeated calculations"
        
        # Both should be reasonably fast
        assert iterative_total_time < 5.0
        assert memoized_total_time < 1.0
    
    def test_generator_memory_efficiency_stress(self):
        """Stress test generator memory efficiency with large sequences."""
        large_counts = [1000, 5000, 10000]
        
        for count in large_counts:
            gen = self.fib.sequence_generator(count)
            
            # Should be able to create generator instantly
            start_time = time.perf_counter()
            first_ten = []
            for i, value in enumerate(gen):
                if i >= 10:
                    break
                first_ten.append(value)
            creation_time = time.perf_counter() - start_time
            
            # Should get first 10 values quickly
            assert creation_time < 0.01, f"Generator too slow for count {count}"
            assert first_ten == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    
    def test_concurrent_access_simulation(self):
        """Simulate concurrent access patterns."""
        # This tests that the FibonacciGenerator is safe for typical usage patterns
        fib1 = FibonacciGenerator()
        fib2 = FibonacciGenerator()
        
        # Each instance should maintain its own cache
        result1_10 = fib1.memoized_recursive(10)
        result2_15 = fib2.memoized_recursive(15)
        
        # Verify independent caches
        assert len(fib1._memo_cache) >= 10
        assert len(fib2._memo_cache) >= 15
        
        # Results should be correct
        assert result1_10 == 55  # F(10)
        assert result2_15 == 610  # F(15)
        
        # Cross-check with fresh calculations
        assert result1_10 == fib2.iterative(10)
        assert result2_15 == fib1.iterative(15)


class TestRobustnessAndErrorHandling:
    """Test system robustness and comprehensive error handling."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fib = FibonacciGenerator()
    
    def test_error_recovery_patterns(self):
        """Test that system recovers gracefully from errors."""
        # Test sequence of operations with intermittent errors
        try:
            self.fib.iterative(-5)  # Should raise error
        except FibonacciError:
            pass  # Expected
        
        # Should be able to continue normal operation
        result = self.fib.iterative(10)
        assert result == 55
        
        # Test invalid method followed by valid operation
        try:
            self.fib.get_sequence(5, 'invalid_method')
        except FibonacciError:
            pass  # Expected
        
        # Should still work normally
        valid_sequence = self.fib.get_sequence(5, 'iterative')
        assert valid_sequence == [0, 1, 1, 2, 3]
    
    def test_input_validation_comprehensive(self):
        """Comprehensive test of input validation across all methods."""
        invalid_inputs = [-1, -10, -100]
        
        for invalid_n in invalid_inputs:
            # Test all calculation methods
            with pytest.raises(FibonacciError):
                self.fib.iterative(invalid_n)
            
            with pytest.raises(FibonacciError):
                self.fib.recursive(invalid_n)
            
            with pytest.raises(FibonacciError):
                self.fib.memoized_recursive(invalid_n)
            
            # Test sequence generation methods
            with pytest.raises(FibonacciError):
                self.fib.get_sequence(invalid_n)
            
            with pytest.raises(FibonacciError):
                list(self.fib.sequence_generator(invalid_n))
    
    def test_boundary_value_comprehensive(self):
        """Comprehensive boundary value testing."""
        boundary_values = [0, 1, 2]
        
        for n in boundary_values:
            # All methods should produce consistent results
            iterative_result = self.fib.iterative(n)
            recursive_result = self.fib.recursive(n)
            memoized_result = self.fib.memoized_recursive(n)
            
            assert iterative_result == recursive_result == memoized_result, \
                f"Boundary value F({n}) inconsistent across methods"
            
            # Sequence methods should also be consistent
            sequence_iter = self.fib.get_sequence(n + 1, 'iterative')
            sequence_gen = self.fib.get_sequence(n + 1, 'generator')
            
            assert sequence_iter[n] == iterative_result
            assert sequence_gen[n] == iterative_result
    
    def test_exception_message_quality(self):
        """Test that exception messages are informative and helpful."""
        # Test negative number error message
        with pytest.raises(FibonacciError) as exc_info:
            self.fib.iterative(-5)
        assert "not defined for negative numbers" in str(exc_info.value)
        
        # Test invalid method error message
        with pytest.raises(FibonacciError) as exc_info:
            self.fib.get_sequence(5, 'invalid')
        error_msg = str(exc_info.value)
        assert "Invalid method" in error_msg
        assert "iterative" in error_msg  # Should suggest valid methods
        
        # Test recursive method size limit error
        with pytest.raises(FibonacciError) as exc_info:
            self.fib.get_sequence(40, 'recursive')
        error_msg = str(exc_info.value)
        assert "too slow" in error_msg
        assert "iterative" in error_msg  # Should suggest alternatives


class TestSystemIntegration:
    """Test integration between different system components."""
    
    def test_benchmark_integration_with_methods(self):
        """Test that benchmark function properly integrates with calculation methods."""
        n = 30
        results = benchmark_methods(n)
        
        # Should have timing results for efficient methods
        assert 'iterative' in results
        assert 'memoized_recursive' in results
        assert isinstance(results['iterative'], float)
        assert isinstance(results['memoized_recursive'], float)
        
        # Verify that benchmarked methods actually produce correct results
        fib = FibonacciGenerator()
        expected_result = fib.iterative(n)
        
        # Check that memoized method produces same result
        fib.clear_cache()
        memoized_result = fib.memoized_recursive(n)
        assert memoized_result == expected_result
    
    def test_interactive_interface_method_integration(self):
        """Test that interactive interface properly integrates with calculation methods."""
        test_commands = [
            ('single 12', '144'),        # F(12) = 144
            ('sequence 6 iterative', 'First 6'),
            ('sequence 4 memoized', 'memoized'),
            ('generator 7', 'using generator'),
            ('quit', 'Thank you')
        ]
        
        for command, expected_output in test_commands:
            with patch('builtins.input', side_effect=[command, 'quit']):
                with patch('builtins.print') as mock_print:
                    interactive_interface()
                
                all_output = ' '.join(str(call) for call in mock_print.call_args_list)
                assert expected_output in all_output, \
                    f"Expected '{expected_output}' for command '{command}'"
    
    def test_main_function_integration(self):
        """Test that main function properly integrates all components."""
        # Test help integration
        with patch('sys.argv', ['fibonacci.py', '--help']):
            with patch('builtins.print') as mock_print:
                main()
            
            output = ' '.join(str(call) for call in mock_print.call_args_list)
            assert 'Usage:' in output
            assert 'Interactive mode' in output
        
        # Test calculation integration
        with patch('sys.argv', ['fibonacci.py', '13']):
            with patch('builtins.print') as mock_print:
                main()
            
            output = ' '.join(str(call) for call in mock_print.call_args_list)
            assert '233' in output  # F(13) = 233
        
        # Test interactive mode integration
        with patch('sys.argv', ['fibonacci.py']):
            with patch('fibonacci.interactive_interface') as mock_interactive:
                main()
                mock_interactive.assert_called_once()


class TestRealWorldUsageScenarios:
    """Test realistic usage scenarios and patterns."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fib = FibonacciGenerator()
    
    def test_educational_usage_pattern(self):
        """Test typical educational usage pattern: exploring small sequences."""
        # Student exploring first 10 Fibonacci numbers
        sequence = self.fib.get_sequence(10, 'iterative')
        assert len(sequence) == 10
        assert sequence == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        
        # Student checking individual calculations
        for i, expected in enumerate(sequence):
            assert self.fib.iterative(i) == expected
        
        # Student comparing methods for verification
        for method in ['recursive', 'memoized']:
            if method == 'recursive' or len(sequence) <= 30:
                method_sequence = self.fib.get_sequence(len(sequence), method)
                assert method_sequence == sequence
    
    def test_research_usage_pattern(self):
        """Test typical research usage pattern: exploring large numbers."""
        # Researcher calculating large Fibonacci numbers
        large_indices = [100, 200, 300, 500]
        
        for n in large_indices:
            # Calculate using most efficient method
            result = self.fib.iterative(n)
            assert isinstance(result, int)
            assert result > 0
            
            # Verify with memoized method for consistency
            self.fib.clear_cache()
            memoized_result = self.fib.memoized_recursive(n)
            assert result == memoized_result
    
    def test_application_development_pattern(self):
        """Test typical application development pattern: embedding in larger system."""
        # Simulate using Fibonacci in a larger application
        class ApplicationSimulator:
            def __init__(self):
                self.fib_generator = FibonacciGenerator()
            
            def get_fibonacci_ratio(self, n):
                """Get ratio between consecutive Fibonacci numbers."""
                if n < 2:
                    return None
                fn = self.fib_generator.iterative(n)
                fn_minus_1 = self.fib_generator.iterative(n - 1)
                return fn / fn_minus_1 if fn_minus_1 != 0 else float('inf')
            
            def get_fibonacci_sum(self, count):
                """Get sum of first 'count' Fibonacci numbers."""
                sequence = self.fib_generator.get_sequence(count, 'generator')
                return sum(sequence)
        
        app = ApplicationSimulator()
        
        # Test ratio calculation (should approach golden ratio)
        ratio_20 = app.get_fibonacci_ratio(20)
        ratio_30 = app.get_fibonacci_ratio(30)
        
        assert ratio_20 is not None
        assert ratio_30 is not None
        assert abs(ratio_30 - 1.618033988749) < 0.001  # Close to golden ratio
        
        # Test sum calculation
        sum_10 = app.get_fibonacci_sum(10)
        expected_sum = sum([0, 1, 1, 2, 3, 5, 8, 13, 21, 34])  # = 88
        assert sum_10 == expected_sum
    
    def test_performance_analysis_pattern(self):
        """Test typical performance analysis usage pattern."""
        # Performance analyst comparing different approaches
        test_values = [20, 25, 30, 35]
        
        for n in test_values:
            # Benchmark different methods
            results = benchmark_methods(n)
            
            # Should have timing data for efficient methods
            assert 'iterative' in results
            assert 'memoized_recursive' in results
            
            # Iterative should be consistently fast
            assert isinstance(results['iterative'], float)
            assert results['iterative'] < 1.0  # Should complete quickly
            
            # If recursive is included, it should be slower for larger n
            if 'recursive' in results and isinstance(results['recursive'], float):
                if n >= 30:
                    assert results['recursive'] > results['iterative']


if __name__ == "__main__":
    # Configuration for running integration tests
    print("Running Fibonacci Integration Tests...")
    print("=" * 60)
    
    # Run the tests with appropriate configuration
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--durations=10",
        "-m", "not slow",  # Skip slow tests by default
    ])