#!/usr/bin/env python3
"""
Test Verification Script

This script verifies that the test suite is properly set up and can run basic tests.
Run this script to ensure everything is working before running the full test suite.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    # Add src to path
    src_path = Path(__file__).parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    try:
        from fibonacci import FibonacciGenerator, FibonacciError, benchmark_methods
        print("  + Successfully imported fibonacci module")
    except ImportError as e:
        print(f"  - Failed to import fibonacci module: {e}")
        return False
    
    try:
        import pytest
        print("  + Pytest is available")
    except ImportError:
        print("  - Pytest not found - install with: pip install pytest")
        return False
    
    return True


def test_basic_functionality():
    """Test basic Fibonacci functionality."""
    print("\nTesting basic functionality...")
    
    from fibonacci import FibonacciGenerator
    fib = FibonacciGenerator()
    
    # Test base cases
    assert fib.iterative(0) == 0, "F(0) should be 0"
    assert fib.iterative(1) == 1, "F(1) should be 1"
    print("  + Base cases work correctly")
    
    # Test known values
    known_values = [(5, 5), (10, 55), (15, 610)]
    for n, expected in known_values:
        result = fib.iterative(n)
        assert result == expected, f"F({n}) should be {expected}, got {result}"
    print("  + Known values are correct")
    
    # Test error handling
    try:
        fib.iterative(-1)
        assert False, "Should have raised FibonacciError for negative input"
    except Exception as e:
        assert "negative" in str(e).lower(), f"Expected negative number error, got: {e}"
    print("  + Error handling works correctly")
    
    return True


def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        "src/fibonacci.py",
        "tests/test_fibonacci.py",
        "tests/test_fibonacci_integration.py",
        "tests/conftest.py",
        "pytest.ini",
        "requirements-test.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"  + {file_path} exists")
    
    if missing_files:
        print(f"  - Missing files: {missing_files}")
        return False
    
    return True


def run_sample_test():
    """Run a simple test to verify the test framework works."""
    print("\nRunning sample test...")
    
    # Try to run a simple pytest test
    import subprocess
    
    try:
        # Create a simple test file to verify pytest works
        simple_test = '''
import sys
from pathlib import Path

# Add src to path  
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from fibonacci import FibonacciGenerator

def test_simple():
    fib = FibonacciGenerator()
    assert fib.iterative(5) == 5
'''
        
        with open("tests/test_verification.py", "w") as f:
            f.write(simple_test)
        
        # Run the test
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_verification.py", "-v"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        # Clean up
        Path("tests/test_verification.py").unlink(missing_ok=True)
        
        if result.returncode == 0:
            print("  + Sample pytest test ran successfully")
            return True
        else:
            print(f"  - Sample pytest test failed:")
            print(f"    STDOUT: {result.stdout}")
            print(f"    STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  - Failed to run sample test: {e}")
        return False


def main():
    """Main verification function."""
    print("=" * 50)
    print("Fibonacci Test Suite Verification")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run all verification tests
    tests = [
        test_imports,
        test_basic_functionality,
        test_file_structure,
        run_sample_test
    ]
    
    for test_func in tests:
        try:
            if not test_func():
                all_tests_passed = False
        except Exception as e:
            print(f"  - Test {test_func.__name__} failed with exception: {e}")
            all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("SUCCESS: All verification tests passed!")
        print("\nYou can now run the full test suite with:")
        print("  python run_tests.py")
        print("  or: pytest tests/ -v")
    else:
        print("FAILURE: Some verification tests failed!")
        print("\nPlease fix the issues above before running the full test suite.")
    print("=" * 50)
    
    return 0 if all_tests_passed else 1


if __name__ == "__main__":
    sys.exit(main())