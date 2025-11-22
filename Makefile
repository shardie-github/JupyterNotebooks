.PHONY: ci lint type-check test test-unit test-integration format install clean help

help:
	@echo "Available commands:"
	@echo "  make ci              - Run all CI checks (lint, type-check, test-unit)"
	@echo "  make lint            - Run linters (ruff + black check)"
	@echo "  make format          - Format code (black + ruff fix)"
	@echo "  make type-check      - Run type checker (mypy)"
	@echo "  make test            - Run all tests"
	@echo "  make test-unit       - Run unit tests only (fast, no I/O)"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-cov        - Run tests with coverage report"
	@echo "  make install         - Install dependencies"
	@echo "  make clean           - Clean cache and build artifacts"

ci: lint type-check test-unit

lint:
	@echo "Running ruff..."
	ruff check agent_factory/ tests/
	@echo "Running black check..."
	black --check agent_factory/ tests/

format:
	@echo "Formatting with black..."
	black agent_factory/ tests/
	@echo "Fixing with ruff..."
	ruff check --fix agent_factory/ tests/

type-check:
	@echo "Running mypy..."
	mypy agent_factory/ --ignore-missing-imports

test:
	@echo "Running all tests..."
	pytest tests/ -v

test-unit:
	@echo "Running unit tests..."
	pytest tests/ -m "not integration and not slow" -v

test-integration:
	@echo "Running integration tests..."
	pytest tests/ -m integration -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ -m "not integration and not slow" -v --cov=agent_factory --cov-report=html --cov-report=term

install:
	@echo "Installing dependencies..."
	pip install -e ".[dev]"

clean:
	@echo "Cleaning cache and build artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "Clean complete."
