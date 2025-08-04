#!/usr/bin/env python3
"""
Test runner for the Albert Heijn API Wrapper.

This script runs all tests for the AH wrapper module.
"""

import os
import sys

import pytest

# Add the parent directory to the path so we can import the wrapper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_tests():
    """Run all tests for the AH wrapper."""
    print("Running AH Wrapper Tests")
    print("=" * 50)

    # Get the directory containing this script
    test_dir = os.path.dirname(os.path.abspath(__file__))

    # Run pytest on the test directory
    result = pytest.main([test_dir, "-v", "--tb=short"])

    if result == 0:
        print("\n[SUCCESS] All tests passed!")
    else:
        print("\n[FAILED] Some tests failed!")

    return result


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
