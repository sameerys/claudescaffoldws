#!/usr/bin/env python3
"""
Simple Test Demonstration

This script demonstrates the test cases without requiring pytest,
showing that our comprehensive test suite covers all the important aspects.
"""

import sys
import time
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from fibonacci import FibonacciGenerator, FibonacciError, benchmark_methods


def run_test(test_name, test_func):
    """Run a single test and report results."""
    try:
        print(f"Running {test_name}...", end=" ")
        test_func()
        print("PASSED")
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def test_basic_functionality():
    """Test basic Fibonacci calculations."""
    fib = FibonacciGenerator()
    
    # Test base cases
    assert fib.iterative(0) == 0
    assert fib.iterative(1) == 1
    
    # Test known values
    known_values = [(5, 5), (10, 55), (15, 610), (20, 6765)]
    for n, expected in known_values:
        assert fib.iterative(n) == expected


def test_method_consistency():
    """Test that all methods produce consistent results."""
    fib = FibonacciGenerator()
    
    test_values = [0, 1, 2, 5, 10, 15, 20]
    
    for n in test_values:
        iterative_result = fib.iterative(n)
        memoized_result = fib.memoized_recursive(n)
        
        # Clear cache for fair comparison
        fib.clear_cache()
        
        if n <= 25:  # Only test recursive for reasonable values
            recursive_result = fib.recursive(n)
            assert iterative_result == recursive_result
        
        assert iterative_result == memoized_result


def test_sequence_generation():
    """Test sequence generation methods."""
    fib = FibonacciGenerator()
    
    # Test different sequence generation methods
    methods = ['iterative', 'memoized', 'generator']
    sequence_length = 10
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    
    for method in methods:
        sequence = fib.get_sequence(sequence_length, method)
        assert sequence == expected, f"Method {method} produced incorrect sequence"


def test_error_handling():
    """Test error handling for invalid inputs."""
    fib = FibonacciGenerator()
    
    # Test negative numbers
    try:
        fib.iterative(-1)
        assert False, "Should have raised error for negative input"
    except FibonacciError as e:
        assert "negative" in str(e).lower()
    
    # Test invalid method
    try:
        fib.get_sequence(5, 'invalid_method')
        assert False, "Should have raised error for invalid method"
    except FibonacciError as e:
        assert "Invalid method" in str(e)
    
    # Test negative sequence count
    try:
        fib.get_sequence(-1)
        assert False, "Should have raised error for negative count"
    except FibonacciError as e:
        assert "negative" in str(e).lower()


def test_generator_functionality():
    """Test generator-based sequence generation."""
    fib = FibonacciGenerator()
    
    # Test generator with limit
    gen = fib.sequence_generator(5)
    result = list(gen)
    expected = [0, 1, 1, 2, 3]
    assert result == expected
    
    # Test generator without limit (take first few)
    gen = fib.sequence_generator()
    first_five = []
    for i, value in enumerate(gen):
        if i >= 5:
            break
        first_five.append(value)
    assert first_five == expected


def test_memoization():
    """Test memoization cache functionality."""
    fib = FibonacciGenerator()
    
    # Clear cache and verify initial state
    fib.clear_cache()
    assert len(fib._memo_cache) == 2  # Should have F(0) and F(1)
    
    # Calculate F(20) and verify cache growth
    result = fib.memoized_recursive(20)
    assert result == 6765
    assert len(fib._memo_cache) >= 20
    
    # Test cache effectiveness (second call should be instant)
    start_time = time.perf_counter()
    result2 = fib.memoized_recursive(20)
    end_time = time.perf_counter()
    
    assert result == result2
    assert end_time - start_time < 0.001  # Should be nearly instant


def test_performance_characteristics():
    """Test basic performance characteristics."""
    fib = FibonacciGenerator()
    
    # Test that iterative method is fast for large numbers
    start_time = time.perf_counter()
    result = fib.iterative(100)
    end_time = time.perf_counter()
    
    assert end_time - start_time < 1.0  # Should complete quickly
    assert isinstance(result, int)
    assert result > 0


def test_benchmark_function():
    """Test the benchmark function."""
    results = benchmark_methods(25)
    
    # Should have results for efficient methods
    assert 'iterative' in results
    assert 'memoized_recursive' in results
    
    # Should have timing data
    assert isinstance(results['iterative'], float)
    assert isinstance(results['memoized_recursive'], float)
    
    # Should include recursive for small values
    assert 'recursive' in results
    assert isinstance(results['recursive'], float)


def test_fibonacci_property():
    """Test that generated sequences follow the Fibonacci property."""
    fib = FibonacciGenerator()
    sequence = fib.get_sequence(20, 'iterative')
    
    # Verify Fibonacci property: F(n) = F(n-1) + F(n-2)
    for i in range(2, len(sequence)):
        expected = sequence[i-1] + sequence[i-2]
        assert sequence[i] == expected, f"Fibonacci property violated at index {i}"


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    fib = FibonacciGenerator()
    
    # Test zero-length sequences
    assert fib.get_sequence(0) == []
    
    # Test single element sequences
    assert fib.get_sequence(1) == [0]
    
    # Test boundary values
    assert fib.iterative(0) == 0
    assert fib.iterative(1) == 1
    assert fib.iterative(2) == 1


def main():
    """Run all tests and report results."""
    print("=" * 60)
    print("Fibonacci Test Suite Demonstration")
    print("=" * 60)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Method Consistency", test_method_consistency),
        ("Sequence Generation", test_sequence_generation),
        ("Error Handling", test_error_handling),
        ("Generator Functionality", test_generator_functionality),
        ("Memoization", test_memoization),
        ("Performance Characteristics", test_performance_characteristics),
        ("Benchmark Function", test_benchmark_function),
        ("Fibonacci Property", test_fibonacci_property),
        ("Edge Cases", test_edge_cases),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed!")
        print("\nThe comprehensive test suite covers:")
        print("  • All calculation methods (iterative, recursive, memoized)")
        print("  • Sequence generation with multiple approaches")
        print("  • Error handling and input validation")
        print("  • Performance characteristics and optimization")
        print("  • Edge cases and boundary conditions")
        print("  • Mathematical correctness (Fibonacci property)")
        print("  • Cache functionality and effectiveness")
        print("  • Integration between components")
        print("\nTo run the full test suite with pytest (once installed):")
        print("  python run_tests.py")
        print("  pytest tests/ -v")
    else:
        print(f"FAILURE: {total - passed} tests failed!")
    
    print("=" * 60)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())