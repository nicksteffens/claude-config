#!/bin/bash
# Test runner for Claude Code agent tests

set -e

cd "$(dirname "$0")"

echo "=== Claude Code Agent Test Runner ==="
echo

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install/upgrade dependencies
echo "Installing test dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements-test.txt

echo
echo "=== Running Tests ==="
echo

# Parse command line arguments
case "${1:-all}" in
    all)
        echo "Running all tests..."
        pytest integration/ -v
        ;;
    daily-log)
        echo "Running daily-log tests..."
        pytest integration/daily_log/ -v
        ;;
    critical)
        echo "Running critical tests (known bugs)..."
        pytest -m critical -v
        ;;
    security)
        echo "Running security tests..."
        pytest -m security -v
        ;;
    coverage)
        echo "Running tests with coverage..."
        pytest --cov=lib --cov=integration --cov-report=term-missing --cov-report=html
        echo
        echo "Coverage report generated in htmlcov/index.html"
        ;;
    *)
        echo "Usage: $0 [all|daily-log|critical|security|coverage]"
        echo
        echo "Options:"
        echo "  all       - Run all tests (default)"
        echo "  daily-log - Run only daily-log skill tests"
        echo "  critical  - Run only critical tests for known bugs"
        echo "  security  - Run only security tests"
        echo "  coverage  - Run tests with coverage report"
        exit 1
        ;;
esac

echo
echo "=== Test run complete ==="
