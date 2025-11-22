# Contributing to Agent Factory Platform

Thank you for contributing to Agent Factory Platform! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/agent-factory.git
   cd agent-factory
   ```

2. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run tests locally:**
   ```bash
   make test-unit      # Fast unit tests
   make test           # All tests
   make ci             # All CI checks (lint, type-check, test-unit)
   ```

## Running CI Checks Locally

Before submitting a PR, run the same checks that CI runs:

```bash
# Run all CI checks
make ci

# Or run individually
make lint          # Run linters (ruff + black check)
make type-check    # Run type checker (mypy)
make test-unit     # Run unit tests only
```

## Code Style

- **Formatting**: We use `black` for code formatting
  ```bash
  make format      # Auto-format code
  ```

- **Linting**: We use `ruff` for linting
  ```bash
  make lint        # Check linting
  ```

- **Type Checking**: We use `mypy` for type checking
  ```bash
  make type-check  # Check types
  ```

## Test Guidelines

### Test Markers

We use pytest markers to categorize tests:

- `@pytest.mark.unit` - Fast unit tests with no external I/O (run in CI)
- `@pytest.mark.integration` - Integration tests requiring external services (run nightly)
- `@pytest.mark.slow` - Slow tests taking >1 second (run nightly)

### Running Tests

```bash
# Unit tests only (fast, runs in CI)
pytest -m unit

# Integration tests only (requires services)
pytest -m integration

# Exclude slow tests
pytest -m "not slow"

# All tests
pytest
```

### Writing Tests

1. **Use fixtures**: Common test objects are available in `tests/conftest.py`
   ```python
   def test_agent(sample_agent):
       assert sample_agent.id == "test-agent"
   ```

2. **Mock external dependencies**: Don't make real API calls in unit tests
   ```python
   @patch('agent_factory.integrations.openai_client.OpenAIAgentClient')
   def test_agent_run(mock_client):
       # Test with mocked client
   ```

3. **Mark tests appropriately**: Use `@pytest.mark.unit`, `@pytest.mark.integration`, or `@pytest.mark.slow`

## Pull Request Process

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure:
   - All tests pass (`make test-unit`)
   - Code is formatted (`make format`)
   - Linting passes (`make lint`)
   - Type checking passes (`make type-check`)

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: Add your feature"
   ```

4. **Push and create a PR:**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Ensure CI passes**: All checks must pass before merge:
   - `lint` - Code style and linting
   - `type-check` - Type checking
   - `test` - Unit tests

## CI Workflow

### PR Checks (Required)

Every PR runs these checks:

- **lint**: Code formatting and linting (ruff + black)
- **type-check**: Type checking (mypy)
- **test**: Unit tests (pytest with unit marker)
- **build**: Docker build (smoke test)

### Nightly Checks (Optional)

These run on a schedule:

- **test-integration**: Full integration test suite with PostgreSQL/Redis
- **security**: Security scans (safety, bandit)

## Common Issues

### Tests Fail Locally But Pass in CI

- Ensure you're running `make test-unit` (not `make test`)
- Check that you have the latest dependencies: `pip install -e ".[dev]"`
- Clear pytest cache: `make clean && make test-unit`

### Type Checking Fails

- Run `mypy agent_factory/` locally to see errors
- Add type annotations to functions missing them
- Use `# type: ignore` sparingly and document why

### Linting Fails

- Run `make format` to auto-fix most issues
- Check `ruff check agent_factory/` for remaining issues

## Questions?

- Open an issue for bugs or feature requests
- Check existing documentation in `docs/`
- Review `CI_STABILIZATION_PLAN.md` for CI details
