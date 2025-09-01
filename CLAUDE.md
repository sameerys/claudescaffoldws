# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python mathematics project containing implementations of mathematical sequence algorithms (Fibonacci and factorial). The project demonstrates multiple algorithmic approaches, comprehensive testing, and professional Python development practices.

## Repository Structure

```
ScaffoldWS/
├── .github/
│   └── copilot-instructions.md  # GitHub Copilot workflow instructions
├── src/                         # Source code
│   ├── factorial.py             # Factorial calculation (iterative & recursive)
│   └── fibonacci.py             # Fibonacci sequence generator (4 implementations)
├── tests/                       # Comprehensive test suite
│   ├── test_fibonacci.py        # Unit tests for Fibonacci methods
│   ├── test_fibonacci_integration.py  # Integration tests
│   ├── conftest.py             # Pytest configuration and fixtures
│   └── README.md               # Test documentation
├── docs/                       # Documentation (currently empty)
├── pytest.ini                 # Test configuration
├── run_tests.py               # Test runner utility
├── verify_tests.py            # Test setup verification
├── simple_test_demo.py        # Working test demonstration
├── requirements-test.txt      # Test dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # Project description
```

## Current Implementation

### **Python Programs:**

1. **Fibonacci Sequence Generator** (`src/fibonacci.py`)
   - Multiple implementations: iterative, recursive, memoized, generator
   - Interactive CLI interface with benchmarking
   - Comprehensive error handling and input validation
   - Time/space complexity analysis in documentation

2. **Factorial Calculator** (`src/factorial.py`)
   - Iterative and recursive implementations
   - Interactive user interface
   - Complete error handling and type hints

### **Testing Framework:**
- **pytest-based** comprehensive test suite
- **100+ test cases** covering all methods and edge cases
- **Performance testing** and benchmarking integration
- **Integration tests** for CLI interfaces
- **Automated test runners** and verification scripts

## Development Workflow

### **Testing Commands:**
```bash
# Run all tests
python run_tests.py

# Run specific test categories
pytest -m "not slow"              # Skip performance tests
pytest tests/test_fibonacci.py   # Unit tests only
pytest -v                        # Verbose output
```

### **Program Execution:**
```bash
# Fibonacci generator
python src/fibonacci.py 10
python src/fibonacci.py 15 sequence

# Factorial calculator  
python src/factorial.py
```

## Code Quality Standards

- **Type hints** throughout all code
- **Comprehensive docstrings** with complexity analysis
- **Error handling** with custom exception classes
- **Professional structure** with classes and separation of concerns
- **Performance awareness** with algorithmic complexity documentation
- **Interactive interfaces** with user-friendly error messages

## Testing Strategy

- **Unit tests** for individual methods
- **Integration tests** for CLI interfaces
- **Performance benchmarks** for algorithm comparison
- **Edge case coverage** (zero, negative, large numbers)
- **Error scenario testing** for exception handling

## Key Guidelines

- Follow existing code patterns and documentation style
- Maintain comprehensive test coverage for new features
- Use type hints and docstrings for all functions
- Include performance considerations in implementations
- Provide both educational and practical algorithm variants