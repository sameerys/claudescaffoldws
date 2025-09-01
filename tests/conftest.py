"""
Pytest configuration and fixtures for Fibonacci tests.

This file provides shared fixtures, configuration, and utilities
for all test files in the test suite.
"""

import pytest
import sys
import os
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


@pytest.fixture
def fibonacci_generator():
    """Provide a fresh FibonacciGenerator instance for tests."""
    from fibonacci import FibonacciGenerator
    return FibonacciGenerator()


@pytest.fixture
def fibonacci_generator_with_cache():
    """Provide a FibonacciGenerator with pre-populated cache for testing."""
    from fibonacci import FibonacciGenerator
    fib = FibonacciGenerator()
    # Pre-populate cache with first 20 Fibonacci numbers
    for i in range(20):
        fib.memoized_recursive(i)
    return fib


@pytest.fixture
def expected_fibonacci_sequence():
    """Provide expected Fibonacci sequence values for testing."""
    return [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 
            610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368]


@pytest.fixture
def sample_test_cases():
    """Provide sample test cases with inputs and expected outputs."""
    return [
        (0, 0),
        (1, 1),
        (2, 1),
        (5, 5),
        (10, 55),
        (15, 610),
        (20, 6765),
        (25, 75025),
    ]


def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their names and locations."""
    for item in items:
        # Mark slow tests
        if "stress" in item.name or "large_number" in item.name or "performance" in item.name:
            item.add_marker(pytest.mark.slow)
        
        # Mark integration tests
        if "integration" in item.fspath.basename or "end_to_end" in item.name:
            item.add_marker(pytest.mark.integration)
        
        # Mark performance tests
        if "benchmark" in item.name or "performance" in item.name:
            item.add_marker(pytest.mark.performance)


@pytest.fixture(autouse=True)
def cleanup_after_test(request):
    """Automatically cleanup after each test."""
    yield
    # Cleanup code runs after each test
    # This ensures test isolation
    pass


# Custom assertion helpers
def assert_fibonacci_property(sequence):
    """Assert that a sequence follows the Fibonacci property F(n) = F(n-1) + F(n-2)."""
    if len(sequence) < 3:
        return True
    
    for i in range(2, len(sequence)):
        expected = sequence[i-1] + sequence[i-2]
        assert sequence[i] == expected, f"Fibonacci property violated at index {i}: {sequence[i]} != {expected}"
    
    return True


def assert_golden_ratio_approximation(fib_ratio, tolerance=0.001):
    """Assert that a Fibonacci ratio approximates the golden ratio."""
    golden_ratio = 1.6180339887498948
    assert abs(fib_ratio - golden_ratio) < tolerance, \
        f"Ratio {fib_ratio} does not approximate golden ratio {golden_ratio} within tolerance {tolerance}"


# Make assertion helpers available to all tests
pytest.assert_fibonacci_property = assert_fibonacci_property
pytest.assert_golden_ratio_approximation = assert_golden_ratio_approximation