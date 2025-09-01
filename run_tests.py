#!/usr/bin/env python3
"""
Test Runner for Fibonacci Project

This script provides convenient ways to run different types of tests
with appropriate configurations and reporting.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run only unit tests
    python run_tests.py --integration      # Run only integration tests
    python run_tests.py --performance      # Run only performance tests
    python run_tests.py --fast             # Run all tests except slow ones
    python run_tests.py --coverage         # Run with coverage reporting
    python run_tests.py --verbose          # Run with verbose output
    python run_tests.py --help             # Show this help message

Author: Generated for ScaffoldWS Project
Date: 2025-09-01
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description="Running command"):
    """Run a command and return the result."""
    print(f"\n{description}...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False


def check_pytest_installed():
    """Check if pytest is installed and install if necessary."""
    try:
        import pytest
        return True
    except ImportError:
        print("Pytest not found. Installing test dependencies...")
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"]
        if run_command(cmd, "Installing test dependencies"):
            try:
                import pytest
                return True
            except ImportError:
                print("Failed to install pytest. Please install manually:")
                print("pip install pytest")
                return False
        return False


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(
        description="Run Fibonacci project tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Test selection options
    parser.add_argument(
        "--unit", 
        action="store_true",
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration", 
        action="store_true",
        help="Run only integration tests"
    )
    parser.add_argument(
        "--performance", 
        action="store_true",
        help="Run only performance tests"
    )
    parser.add_argument(
        "--fast", 
        action="store_true",
        help="Run all tests except slow ones"
    )
    
    # Output and reporting options
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Run with coverage reporting"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Run with verbose output"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Run with minimal output"
    )
    
    # Advanced options
    parser.add_argument(
        "--parallel", "-n",
        type=int,
        metavar="NUM",
        help="Run tests in parallel (requires pytest-xdist)"
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run performance benchmarks (requires pytest-benchmark)"
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install test dependencies and exit"
    )
    
    args = parser.parse_args()
    
    # Change to project root directory
    project_root = get_project_root()
    os.chdir(project_root)
    
    # Install dependencies if requested
    if args.install_deps:
        requirements_file = project_root / "requirements-test.txt"
        if requirements_file.exists():
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
            success = run_command(cmd, "Installing test dependencies")
            sys.exit(0 if success else 1)
        else:
            print(f"Requirements file not found: {requirements_file}")
            sys.exit(1)
    
    # Check if pytest is installed
    if not check_pytest_installed():
        sys.exit(1)
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add test selection options
    test_markers = []
    if args.unit:
        test_markers.append("unit")
    if args.integration:
        test_markers.append("integration")
    if args.performance:
        test_markers.append("performance")
    if args.fast:
        test_markers.append("not slow")
    
    if test_markers:
        cmd.extend(["-m", " or ".join(f"({marker})" for marker in test_markers)])
    elif args.fast:
        cmd.extend(["-m", "not slow"])
    
    # Add output options
    if args.verbose:
        cmd.append("-v")
    elif args.quiet:
        cmd.append("-q")
    else:
        cmd.append("-v")  # Default to verbose
    
    # Add coverage options
    if args.coverage:
        cmd.extend([
            "--cov=src",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-report=xml"
        ])
    
    # Add parallel execution
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])
    
    # Add benchmark options
    if args.benchmark:
        cmd.append("--benchmark-only")
    
    # Add other useful options
    cmd.extend([
        "--tb=short",           # Short traceback format
        "--strict-markers",     # Fail on unknown markers
        "--durations=10",       # Show 10 slowest tests
    ])
    
    # Specify test directory
    cmd.append("tests/")
    
    # Run the tests
    print("=" * 60)
    print("🧪 Fibonacci Project Test Suite")
    print("=" * 60)
    
    if args.unit:
        print("Running UNIT tests only...")
    elif args.integration:
        print("Running INTEGRATION tests only...")
    elif args.performance:
        print("Running PERFORMANCE tests only...")
    elif args.fast:
        print("Running FAST tests (excluding slow tests)...")
    else:
        print("Running ALL tests...")
    
    success = run_command(cmd, "Running pytest")
    
    # Print summary
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests completed successfully!")
        if args.coverage:
            print("📊 Coverage report generated in htmlcov/ directory")
    else:
        print("❌ Some tests failed!")
    print("=" * 60)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()