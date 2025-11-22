#!/bin/bash
# Quick test script for solo operators

set -e

echo "🧪 Running quick test suite..."

# Run unit tests (fast, no external services)
pytest tests/ -m "not integration and not slow" -v --tb=short

echo ""
echo "✅ Quick tests passed!"
