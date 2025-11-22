#!/bin/bash
# Development setup script for solo operators

set -e

echo "🚀 Setting up Agent Factory development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -e ".[dev]"

# Run basic checks
echo "🔍 Running basic checks..."

echo "  - Linting..."
ruff check agent_factory/ tests/ || echo "  ⚠ Linting issues found (run 'make format' to fix)"

echo "  - Type checking..."
mypy agent_factory/ --ignore-missing-imports || echo "  ⚠ Type checking issues found"

echo "  - Running tests..."
pytest tests/ -m "not integration and not slow" -v || echo "  ⚠ Some tests failed"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Quick commands:"
echo "  make lint          - Run linters"
echo "  make format        - Auto-format code"
echo "  make test          - Run all tests"
echo "  make test-unit     - Run unit tests only"
echo "  make ci            - Run all CI checks"
