# Fibonacci Test Suite Documentation

This comprehensive test suite validates all aspects of the Fibonacci program implementation, ensuring correctness, performance, and robustness across all methods and use cases.

## Test Structure Overview

```
tests/
├── conftest.py                    # Pytest configuration and shared fixtures
├── test_fibonacci.py             # Core unit tests for all methods
├── test_fibonacci_integration.py # Integration and end-to-end tests
├── run_tests.py                  # Test runner script (in parent directory)
└── README.md                     # This documentation file
```

## Test Categories

### 1. Unit Tests (`test_fibonacci.py`)

**Core Functionality Tests:**
- `TestIterativeMethod`: Tests for the iterative Fibonacci calculation
- `TestRecursiveMethod`: Tests for the recursive Fibonacci calculation  
- `TestMemoizedRecursiveMethod`: Tests for the memoized recursive approach
- `TestSequenceGenerator`: Tests for the generator-based sequence creation
- `TestGetSequenceMethod`: Tests for the unified sequence generation interface

**Supporting Component Tests:**
- `TestFibonacciError`: Custom exception handling tests
- `TestBenchmarkMethods`: Performance benchmarking functionality tests
- `TestInteractiveInterface`: Interactive command-line interface tests
- `TestMainFunction`: Main function and command-line argument tests

**Edge Case and Boundary Tests:**
- `TestEdgeCasesAndBoundaryConditions`: Comprehensive edge case coverage
- `TestPerformanceCharacteristics`: Performance behavior validation

### 2. Integration Tests (`test_fibonacci_integration.py`)

**End-to-End Workflow Tests:**
- `TestEndToEndWorkflows`: Complete calculation and interface workflows
- `TestSystemIntegration`: Integration between different components

**Stress and Performance Tests:**
- `TestStressAndPerformance`: High-load and large-number testing
- `TestRealWorldUsageScenarios`: Realistic usage pattern simulation

**Robustness Tests:**
- `TestRobustnessAndErrorHandling`: Error recovery and input validation

## Test Coverage Areas

### ✅ Method Testing
- **Iterative Method**: Base cases, small/large numbers, negative inputs, performance
- **Recursive Method**: Base cases, consistency with iterative, performance limits
- **Memoized Recursive**: Cache functionality, performance advantages, large numbers
- **Generator Method**: Memory efficiency, unlimited generation, boundary cases
- **Sequence Generation**: All methods, method consistency, error handling

### ✅ Edge Cases and Boundaries
- Zero and one (base cases)
- Negative numbers (error conditions)
- Very large numbers (performance and accuracy)
- Empty sequences and single-element sequences
- Method switching and consistency validation

### ✅ Error Handling
- `FibonacciError` exception testing
- Invalid input validation across all methods
- Error message quality and informativeness
- Recovery from error conditions
- Input type validation

### ✅ Performance Characteristics
- Linear time complexity validation for iterative method
- Exponential behavior awareness for recursive method
- Memoization effectiveness testing
- Memory efficiency of generator approach
- Comparative performance analysis

### ✅ Interactive Interface
- Command parsing and execution
- All supported commands (single, sequence, generator, benchmark, help, quit)
- Error handling in interactive mode
- Input validation and user feedback
- Session state management

### ✅ Integration and System Testing
- Component integration validation
- End-to-end workflow testing
- Command-line interface testing
- Benchmark integration with calculation methods
- Real-world usage pattern simulation

## Running the Tests

### Quick Start
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
python run_tests.py

# Or use pytest directly
pytest tests/ -v
```

### Test Selection Options

```bash
# Run only unit tests
python run_tests.py --unit

# Run only integration tests
python run_tests.py --integration

# Run only performance tests
python run_tests.py --performance

# Run fast tests only (exclude slow tests)
python run_tests.py --fast

# Run with coverage reporting
python run_tests.py --coverage

# Run tests in parallel (if pytest-xdist installed)
python run_tests.py --parallel 4
```

### Pytest Direct Usage

```bash
# Basic test run
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test categories
pytest tests/ -m "unit"
pytest tests/ -m "integration"
pytest tests/ -m "not slow"

# Run specific test file
pytest tests/test_fibonacci.py -v

# Run specific test class
pytest tests/test_fibonacci.py::TestIterativeMethod -v

# Run specific test method
pytest tests/test_fibonacci.py::TestIterativeMethod::test_iterative_base_cases -v
```

## Test Markers

The test suite uses pytest markers to categorize tests:

- `@pytest.mark.unit`: Unit tests focusing on individual components
- `@pytest.mark.integration`: Integration tests validating component interactions
- `@pytest.mark.slow`: Tests that take significant time to complete
- `@pytest.mark.performance`: Performance and benchmarking tests

Use markers to run specific test categories:
```bash
pytest -m "unit and not slow"           # Fast unit tests only
pytest -m "integration"                 # Integration tests only  
pytest -m "performance"                 # Performance tests only
```

## Test Fixtures and Utilities

### Available Fixtures (`conftest.py`)

- `fibonacci_generator`: Fresh FibonacciGenerator instance
- `fibonacci_generator_with_cache`: Pre-populated cache for testing
- `expected_fibonacci_sequence`: Known correct Fibonacci values
- `sample_test_cases`: Common input/output test pairs

### Custom Assertions

- `assert_fibonacci_property(sequence)`: Validates F(n) = F(n-1) + F(n-2)
- `assert_golden_ratio_approximation(ratio)`: Validates golden ratio approximation

## Coverage Expectations

The test suite aims for comprehensive coverage:

- **Function Coverage**: 100% of all functions and methods
- **Branch Coverage**: All conditional paths and error conditions
- **Edge Case Coverage**: Boundary values and exceptional inputs
- **Integration Coverage**: All component interactions and workflows

### Coverage Report Generation

```bash
# Generate HTML coverage report
python run_tests.py --coverage

# View coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html # Windows
```

## Performance Test Considerations

### Slow Test Management

Some tests are marked as `slow` because they:
- Test very large Fibonacci numbers (F(1000+))
- Perform stress testing with multiple iterations
- Validate performance characteristics over time

Skip slow tests during development:
```bash
pytest -m "not slow"
python run_tests.py --fast
```

### Performance Benchmarks

Performance tests validate:
- **Iterative method**: O(n) time complexity
- **Recursive method**: Exponential time awareness
- **Memoized method**: Caching effectiveness
- **Generator method**: Memory efficiency

## Troubleshooting

### Common Issues

**Import Errors:**
```
ModuleNotFoundError: No module named 'fibonacci'
```
- Ensure you're running tests from the project root directory
- Check that `src/fibonacci.py` exists and is readable

**Missing Dependencies:**
```
ModuleNotFoundError: No module named 'pytest'
```
- Install test dependencies: `pip install -r requirements-test.txt`
- Or install pytest directly: `pip install pytest`

**Slow Test Timeouts:**
- Use `--fast` flag to skip slow tests during development
- Adjust timeout values in `pytest.ini` if needed

### Debug Mode

Run tests in debug mode for detailed investigation:
```bash
# Run with PDB on failures
pytest tests/ --pdb

# Run single test with maximum verbosity
pytest tests/test_fibonacci.py::TestIterativeMethod::test_iterative_base_cases -vvv -s
```

## Contributing to Tests

### Adding New Tests

1. **Unit Tests**: Add to `test_fibonacci.py` in appropriate test class
2. **Integration Tests**: Add to `test_fibonacci_integration.py`
3. **New Test Files**: Follow naming convention `test_*.py`

### Test Writing Guidelines

1. **Descriptive Names**: Use clear, descriptive test method names
2. **AAA Pattern**: Follow Arrange-Act-Assert structure
3. **Single Responsibility**: Each test should validate one specific behavior
4. **Independence**: Tests should not depend on other tests
5. **Documentation**: Include docstrings for complex test logic

### Example New Test

```python
def test_new_fibonacci_behavior(self, fibonacci_generator):
    """Test description explaining what behavior is being validated."""
    # Arrange
    fib = fibonacci_generator
    test_input = 10
    
    # Act
    result = fib.iterative(test_input)
    
    # Assert
    assert result == 55, f"Expected F(10)=55, got {result}"
```

## Continuous Integration

The test suite is designed to work well in CI/CD environments:

```bash
# CI-friendly test run
pytest tests/ --tb=short --quiet --durations=10 --strict-markers

# With coverage for CI reporting
pytest tests/ --cov=src --cov-report=xml --cov-report=term
```

## Summary

This comprehensive test suite ensures the Fibonacci program is:
- **Correct**: All methods produce accurate results
- **Robust**: Handles edge cases and error conditions gracefully
- **Performant**: Meets expected performance characteristics
- **Maintainable**: Well-structured and documented test code
- **Reliable**: Consistent behavior across different usage patterns

The test suite serves as both validation and documentation of the expected behavior of the Fibonacci program, making it easier to maintain and extend the codebase with confidence.