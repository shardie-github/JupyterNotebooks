# Development Workflow for Solo Operators

A guide to working efficiently on Agent Factory as a solo developer or small team.

## Daily Workflow

### Starting Your Day

```bash
# Pull latest changes
git pull

# Run quick tests to make sure everything still works
./scripts/quick_test.sh

# Check for any linting issues
make lint
```

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes**
   - Write code
   - Write tests
   - Update documentation

3. **Test locally**
   ```bash
   # Quick unit tests
   make test-unit
   
   # Full test suite (if needed)
   make test
   
   # All CI checks
   make ci
   ```

4. **Format code**
   ```bash
   make format
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add feature X"
   git push origin feature/my-feature
   ```

## Common Tasks

### Adding a New Module

1. Create the module in `agent_factory/`
2. Add `__init__.py` with exports
3. Write tests in `tests/test_<module>.py`
4. Update documentation
5. Run tests: `pytest tests/test_<module>.py`

### Fixing a Bug

1. Write a failing test that reproduces the bug
2. Fix the bug
3. Verify the test passes
4. Run full test suite: `make test`

### Updating Dependencies

1. Update `pyproject.toml`
2. Run `pip install -e ".[dev]"`
3. Test: `make test`
4. Commit changes

## Testing Strategy

**Unit Tests** (fast, run frequently)
- No external services
- Mock dependencies
- Run with: `make test-unit`

**Integration Tests** (slower, run before commits)
- May require services
- Test real integrations
- Run with: `pytest tests/integration/`

**CI Tests** (run before pushing)
- All checks: `make ci`
- Same as what CI runs

## Debugging

### Import Issues
```bash
# Check imports
python3 -c "import agent_factory; print('OK')"

# Check specific module
python3 -c "from agent_factory.telemetry import TelemetryCollector; print('OK')"
```

### Test Failures
```bash
# Run with verbose output
pytest tests/test_specific.py -vv

# Run with print statements
pytest tests/test_specific.py -s

# Run single test
pytest tests/test_specific.py::test_function_name -vv
```

### Type Checking
```bash
# Check specific file
mypy agent_factory/module.py

# Check with more detail
mypy agent_factory/module.py --show-error-codes
```

## Code Quality

### Before Committing

Run these checks:
```bash
make ci
```

This runs:
- Linting (ruff)
- Formatting check (black)
- Type checking (mypy)
- Unit tests

### Auto-fix Issues

```bash
# Format code
make format

# Some linting issues can be auto-fixed
ruff check --fix agent_factory/ tests/
```

## Documentation

### Updating README
- Keep it simple and clear
- Focus on what users need
- Update examples if APIs change

### Adding Docstrings
- Use Google-style docstrings
- Include examples for complex functions
- Document parameters and return values

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Run full test suite: `make test`
4. Tag release: `git tag v0.1.0`
5. Push tags: `git push --tags`

## Getting Help

- Check existing issues on GitHub
- Read the code (it's well-documented)
- Check test files for usage examples
- Review documentation in `docs/`

## Time-Saving Tips

1. **Use the scripts**
   - `./scripts/dev_setup.sh` - Initial setup
   - `./scripts/quick_test.sh` - Quick validation

2. **Run tests often**
   - Catch issues early
   - Unit tests are fast

3. **Use make commands**
   - `make ci` - Run everything
   - `make format` - Auto-format
   - `make test-unit` - Fast tests

4. **Keep tests simple**
   - Mock external dependencies
   - Test one thing at a time
   - Use fixtures for common setup

5. **Document as you go**
   - Update docs with code changes
   - Add examples to docstrings
   - Keep README current

## Common Issues

### Import Errors
- Check `__init__.py` files
- Verify module structure
- Run: `python3 -c "import agent_factory"`

### Test Failures
- Check if tests require external services
- Verify mocks are set up correctly
- Run with `-vv` for more detail

### CI Failures
- Run `make ci` locally first
- Check for linting/formatting issues
- Verify all tests pass

### Type Errors
- Run `mypy` locally
- Check type hints
- Use `--ignore-missing-imports` if needed
