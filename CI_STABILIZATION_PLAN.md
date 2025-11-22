# CI Stabilization & Code Cleanup Plan

**Status**: Comprehensive audit and execution plan  
**Target**: Green CI on every PR, clean maintainable codebase  
**Timeline**: 7-21 days

---

## A. CODE & CI SNAPSHOT

### CODE & STRUCTURE SNAPSHOT

**High-level structure:**
- **Core primitives**: `agent_factory/core/` (Agent, Tool, Workflow, Blueprint, Memory, Guardrails)
- **Infrastructure**: `api/`, `cli/`, `database/`, `cache/`, `security/`, `monitoring/`
- **Features**: `registry/`, `marketplace/`, `integrations/`, `payments/`, `enterprise/`
- **Tests**: `tests/` with basic unit tests for core primitives
- **Examples**: `examples/` with demo scripts
- **Blueprints**: `blueprints/` with YAML configurations

**Key findings:**
1. **Duplicate logging modules**: `agent_factory/utils/logging.py` (basic) vs `agent_factory/monitoring/logging.py` (structured JSON). Both exist but serve different purposes - needs consolidation.
2. **Import inconsistencies**: Some modules import from `agent_factory.core`, others use relative imports inconsistently.
3. **Missing test infrastructure**: No `conftest.py`, no pytest config, no test fixtures for common scenarios (database, cache, API clients).
4. **Heavy dependencies in tests**: Tests may fail due to missing external services (PostgreSQL, Redis, OpenAI API keys).
5. **Type checking gaps**: `mypy` runs with `--ignore-missing-imports`, hiding real type issues.
6. **No test markers**: No separation between unit/integration/slow tests.
7. **API imports may fail**: `agent_factory.api.main` imports from `agent_factory.monitoring` and `agent_factory.security` which may have missing dependencies.

### CI & CHECKS SNAPSHOT

**Current workflow**: `.github/workflows/ci.yml` contains 6 jobs:

1. **`test`** (runs on PR/push):
   - Installs deps
   - Runs pytest with coverage
   - **DUPLICATE**: Also runs `black --check` and `ruff check` (same as `lint` job)
   - Runs `mypy` with `--ignore-missing-imports`
   - Uploads coverage to codecov

2. **`lint`** (runs on PR/push):
   - Installs deps (duplicate install)
   - Runs `ruff check` and `black --check` (duplicate of `test` job)

3. **`security`** (runs on PR/push):
   - Installs deps (duplicate install)
   - Runs `safety check` with `|| true` (never fails!)
   - Runs `bandit` with `|| true` (never fails!)

4. **`build`** (runs after test/lint/security):
   - Builds Docker image
   - Pushes to GHCR

5. **`deploy-staging`** (runs on `develop` branch):
   - Deploys to Kubernetes staging

6. **`deploy-production`** (runs on release):
   - Deploys to Kubernetes production

**Issues identified:**
- **No caching**: Every job reinstalls Python and dependencies from scratch
- **Duplicate work**: `test` and `lint` jobs overlap
- **Security checks never fail**: `|| true` makes them useless
- **No dependency caching**: pip installs happen fresh every time
- **No test isolation**: Tests may interfere with each other
- **Missing pytest config**: No markers, no test discovery patterns
- **Coverage upload may fail**: codecov may not be configured properly

### WHY SO MANY FAILING CHECKS (HYPOTHESES)

1. **Duplicate linting in test job**: Running `black` and `ruff` in both `test` and `lint` jobs means any formatting issue fails twice, doubling the noise.

2. **Security checks silently fail**: `safety check` and `bandit` run with `|| true`, so they never fail the build but may produce confusing output.

3. **Missing test dependencies**: Tests that require PostgreSQL/Redis may fail if services aren't available in CI.

4. **Type checking too lenient**: `--ignore-missing-imports` hides real type errors that could cause runtime failures.

5. **No test isolation**: Tests may share state or fail due to ordering dependencies.

6. **External API dependencies**: Tests that call OpenAI API may fail due to missing keys or rate limits.

7. **Database initialization issues**: `init_db()` in `api/main.py` may fail if database isn't available, causing import-time failures.

8. **Import-time side effects**: Modules like `agent_factory.api.main` execute code at import time (database init, cache setup) which can fail in test environments.

9. **Missing pytest fixtures**: No shared fixtures for common test scenarios (mock agents, tools, workflows).

10. **No test markers**: Can't easily skip slow/integration tests in CI.

---

## B. TARGET STATE (CODE + CI)

### TARGET CODE PRINCIPLES

1. **Single source of truth**: One logging module, one config system, clear module boundaries.
2. **No import-time side effects**: Database init, cache setup, etc. should be lazy or explicit.
3. **Testability first**: Core logic should be testable without external services (use dependency injection).
4. **Type safety**: Strict type checking without `--ignore-missing-imports`; fix or stub missing types.
5. **Clear separation**: Unit tests (fast, no I/O) vs integration tests (slower, may need services).
6. **Consistent naming**: Use consistent patterns (e.g., `Agent`, `Tool`, `Workflow` as nouns; `create_*`, `get_*`, `run_*` as verbs).
7. **Minimal dependencies**: Core modules shouldn't depend on infrastructure (database, cache) unless necessary.

### TARGET CI CHECK SET

**Core checks (run on every PR):**

1. **`lint`** (2-3 min):
   - `ruff check` (linting)
   - `black --check` (formatting)
   - Purpose: Code style consistency

2. **`type-check`** (1-2 min):
   - `mypy agent_factory/` (strict, no `--ignore-missing-imports`)
   - Purpose: Catch type errors before runtime

3. **`test`** (3-5 min):
   - `pytest tests/ -m "not integration and not slow"` (unit tests only)
   - Purpose: Fast feedback on core logic

4. **`build`** (2-4 min):
   - Docker build (smoke test)
   - Purpose: Ensure Dockerfile works

**Optional checks (run on schedule or main branch):**

5. **`test-integration`** (10-15 min, nightly):
   - Full test suite with real services
   - Purpose: Catch integration issues

6. **`security`** (5-10 min, nightly):
   - `safety check` (vulnerability scanning)
   - `bandit` (security linting)
   - Purpose: Security audit

### WHAT TO DISABLE / CONSOLIDATE

**Disable entirely:**
- Nothing - but fix security checks to actually fail when issues are found

**Move to nightly/scheduled:**
- Full integration test suite
- Security scans (safety, bandit)
- Coverage reporting (can run on main branch only)

**Consolidate:**
- Merge `test` and `lint` jobs: lint should be separate, test should only test
- Remove duplicate dependency installs: use caching and matrix if needed
- Combine security checks into single job (but make them fail properly)

---

## C. WORKFLOW REWRITE PLAN

### CURRENT WORKFLOW INVENTORY

**`.github/workflows/ci.yml`**:
- **Purpose**: Main CI/CD pipeline
- **Status**: Needs consolidation and fixes
- **Action**: Rewrite to remove duplication, add caching, fix security checks

### PROPOSED WORKFLOW SET

**1. `ci.yml`** (main PR/push workflow):
```yaml
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -e ".[dev]"
      - run: ruff check agent_factory/ tests/
      - run: black --check agent_factory/ tests/

  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -e ".[dev]"
      - run: mypy agent_factory/ --strict --no-ignore-missing-imports

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -e ".[dev]"
      - run: pytest tests/ -m "not integration and not slow" -v --cov=agent_factory --cov-report=xml
      - uses: codecov/codecov-action@v4
        if: github.event_name == 'pull_request'
        with:
          file: ./coverage.xml

  build:
    needs: [lint, type-check, test]
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          context: .
          file: ./docker/Dockerfile
          push: false  # Only build, don't push on PRs
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

**2. `nightly.yml`** (scheduled heavy checks):
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily
  workflow_dispatch:

jobs:
  test-integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: agent_factory_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -e ".[dev]"
      - run: pytest tests/ -m integration -v

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -e ".[dev]" safety bandit
      - run: safety check --json
      - run: bandit -r agent_factory/ -f json
```

**3. `release.yml`** (deployment):
```yaml
on:
  release:
    types: [published]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          context: .
          file: ./docker/Dockerfile
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.event.release.tag_name }}

  deploy-production:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: azure/setup-kubectl@v3
      - run: |
          echo "${{ secrets.KUBECONFIG_PROD }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig
          kubectl apply -f k8s/ -n agent-factory
          kubectl set image deployment/agent-factory-api \
            api=ghcr.io/${{ github.repository }}:${{ github.event.release.tag_name }} \
            -n agent-factory
```

### MERGE GUARDRAILS

**Required checks for PR merge:**
- `lint` must pass
- `type-check` must pass  
- `test` must pass
- `build` must pass (if changed Dockerfile)

**Optional (non-blocking):**
- Coverage percentage (informational only)
- Security scans (run nightly, not blocking)

**Branch protection rules:**
- Require `lint`, `type-check`, `test` to pass before merge
- Allow admin override for emergencies
- Require at least 1 approval

---

## D. CODE CLEANUP & TEST ARCHITECTURE

### CODE COHESION ISSUES

1. **Duplicate logging**: `utils/logging.py` vs `monitoring/logging.py` - consolidate to one structured logging approach.

2. **Import-time side effects**: 
   - `agent_factory.api.main` calls `init_db()` at module level
   - `agent_factory.api.main` calls `setup_metrics()`, `setup_tracing()` at import time
   - These can fail in test environments

3. **Heavy core dependencies**: 
   - `Agent._execute_agent()` imports `OpenAIAgentClient` at runtime (good) but may fail silently
   - Tests may need OpenAI API keys to pass

4. **Missing abstractions**: 
   - Database models directly imported in marketplace code
   - No repository pattern for data access

5. **Inconsistent error handling**: 
   - Some functions raise exceptions, others return error results
   - No standard error types

6. **Type annotations incomplete**: 
   - Many functions missing return type annotations
   - Generic types not fully specified

### CODE CLEANUP TASKS

1. **Consolidate logging** (`agent_factory/utils/logging.py` → delete, use `monitoring/logging.py` only)
   - Remove `utils/logging.py`
   - Update any imports to use `monitoring.logging`

2. **Lazy database initialization** (`agent_factory/api/main.py`)
   - Move `init_db()` call to startup event handler
   - Don't fail import if database unavailable

3. **Extract test fixtures** (`tests/conftest.py` - create)
   - Fixtures for mock agents, tools, workflows
   - Fixtures for database sessions (in-memory SQLite for tests)
   - Fixtures for cache (mock Redis)

4. **Add pytest markers** (`pytest.ini` - create)
   - `@pytest.mark.unit` - fast unit tests
   - `@pytest.mark.integration` - requires services
   - `@pytest.mark.slow` - slow tests

5. **Mock external APIs in tests**
   - Mock OpenAI API calls in `test_agent.py`
   - Use `responses` or `httpx` mocking

6. **Fix type annotations** (`agent_factory/core/agent.py`, `tool.py`, etc.)
   - Add return types to all methods
   - Fix generic types (e.g., `Dict[str, Any]` → `Dict[str, Any]`)

7. **Remove `--ignore-missing-imports`** (`ci.yml`)
   - Add type stubs for missing dependencies
   - Or properly type-ignore specific imports

8. **Standardize error handling** (`agent_factory/core/`)
   - Create `agent_factory/core/exceptions.py`
   - Define standard exception hierarchy

9. **Extract repository pattern** (`agent_factory/database/repositories.py` - create)
   - Abstract database access from marketplace/API code
   - Make database operations testable

10. **Add dependency injection** (`agent_factory/core/agent.py`)
    - Make `OpenAIAgentClient` injectable (not hardcoded import)
    - Allow mocking in tests

11. **Fix circular imports** (if any)
    - Review import graph
    - Use TYPE_CHECKING for forward references

12. **Consistent naming** (review all modules)
    - Ensure consistent verb/noun patterns
    - Fix any `get_*` vs `fetch_*` inconsistencies

13. **Remove dead code** (if any)
    - Search for unused functions/classes
    - Remove commented-out code

14. **Add docstrings** (missing in some modules)
    - Ensure all public APIs have docstrings
    - Use Google/NumPy style consistently

15. **Separate concerns** (`agent_factory/api/main.py`)
    - Extract middleware setup to separate module
    - Extract route registration

16. **Add validation** (`agent_factory/core/`)
    - Use Pydantic for config validation
    - Validate inputs at boundaries

17. **Fix test isolation** (`tests/`)
    - Ensure tests don't share state
    - Use fixtures for setup/teardown

18. **Add integration test markers** (`tests/test_*.py`)
    - Mark tests that need database/Redis
    - Mark slow tests

19. **Create test utilities** (`tests/utils.py` - create)
    - Helper functions for creating test data
    - Mock factories

20. **Fix import paths** (review all `from agent_factory.*`)
    - Ensure consistent absolute imports
    - Remove any relative imports

### TEST ARCHITECTURE FIXES

**Missing coverage:**
- API routes (no tests for `agent_factory/api/routes/*`)
- CLI commands (no tests for `agent_factory/cli/commands/*`)
- Database models (no tests for `agent_factory/database/models.py`)
- Security modules (no tests for `agent_factory/security/*`)
- Marketplace (no tests for `agent_factory/marketplace/*`)

**Brittle/flaky tests:**
- `test_agent.py` may fail if OpenAI API unavailable
- `test_workflow.py` creates real agents (may need mocking)
- `test_registry.py` uses temp directories (should be fine)

**Test structure improvements:**

1. **Create `tests/conftest.py`**:
   ```python
   import pytest
   from agent_factory.core.agent import Agent
   from agent_factory.core.tool import Tool
   # ... fixtures for common test objects
   ```

2. **Create `pytest.ini`**:
   ```ini
   [pytest]
   markers =
       unit: Fast unit tests (no I/O)
       integration: Integration tests (require services)
       slow: Slow tests (>1s)
   testpaths = tests
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   ```

3. **Add test markers to existing tests**:
   - Mark all current tests as `@pytest.mark.unit`
   - Add `@pytest.mark.integration` for future integration tests

4. **Mock external dependencies**:
   - Use `unittest.mock` or `pytest-mock` for OpenAI API
   - Use in-memory SQLite for database tests
   - Use `fakeredis` for Redis tests

5. **Add test utilities** (`tests/utils.py`):
   - `create_test_agent()` helper
   - `create_test_tool()` helper
   - `create_test_workflow()` helper

**Must-have tests:**

1. **Agent execution** (`tests/test_agent.py`):
   - Test agent.run() with mocked OpenAI API
   - Test guardrails validation
   - Test memory integration
   - Test tool execution

2. **Tool validation** (`tests/test_tool.py`):
   - Test parameter validation
   - Test schema generation
   - Test execution errors

3. **Workflow execution** (`tests/test_workflow.py`):
   - Test step execution
   - Test branching logic
   - Test error handling

4. **Blueprint loading** (`tests/test_blueprint.py`):
   - Test YAML parsing
   - Test validation
   - Test installation

5. **Registry operations** (`tests/test_registry.py`):
   - Test CRUD operations
   - Test serialization/deserialization

---

## E. CI STABILIZATION PLAN

### PHASED CI STABILIZATION PLAN

#### Phase 1: Stop the Bleeding (Days 1-3)

**Goal**: Get CI green immediately by disabling/fixing broken checks.

1. **Fix security checks** (`ci.yml`):
   - Remove `|| true` from `safety check` and `bandit`
   - Make them actually fail on issues

2. **Remove duplicate linting** (`ci.yml`):
   - Remove `black --check` and `ruff check` from `test` job
   - Keep only in `lint` job

3. **Add dependency caching** (`ci.yml`):
   - Use `actions/setup-python@v5` with `cache: 'pip'`
   - Cache pip dependencies between runs

4. **Fix type checking** (`ci.yml`):
   - Remove `--ignore-missing-imports` (or add proper type stubs)
   - Start with `--ignore-missing-imports` but track issues to fix

5. **Skip integration tests in PRs** (`ci.yml`):
   - Add `-m "not integration"` to pytest command
   - Mark any flaky tests as `@pytest.mark.integration`

6. **Mock external APIs in tests** (`tests/test_agent.py`):
   - Mock OpenAI API calls
   - Use `unittest.mock` or `responses` library

7. **Fix database imports** (`agent_factory/api/main.py`):
   - Move `init_db()` to startup event
   - Don't fail on import

8. **Add pytest config** (`pytest.ini`):
   - Create config file with markers
   - Configure test discovery

9. **Add test markers** (`tests/test_*.py`):
   - Mark all current tests as `@pytest.mark.unit`
   - Mark any slow tests as `@pytest.mark.slow`

10. **Create conftest.py** (`tests/conftest.py`):
    - Add fixtures for common test objects
    - Add fixtures for mocked services

#### Phase 2: Fix Core Checks (Days 4-10)

**Goal**: Make lint, type-check, and unit tests reliable and fast.

1. **Fix all linting errors**:
   - Run `ruff check` locally and fix all issues
   - Run `black` to format code
   - Ensure CI passes

2. **Fix type errors**:
   - Remove `--ignore-missing-imports` gradually
   - Add type stubs for missing dependencies
   - Fix return type annotations

3. **Add missing test coverage**:
   - Add tests for API routes (mock FastAPI test client)
   - Add tests for CLI commands (mock Typer runner)
   - Add tests for database models

4. **Improve test reliability**:
   - Ensure all tests are isolated
   - Fix any flaky tests
   - Add proper fixtures

5. **Add test utilities** (`tests/utils.py`):
   - Helper functions for creating test data
   - Mock factories

6. **Fix import-time side effects**:
   - Move all initialization to lazy or explicit calls
   - Ensure modules can be imported in tests

7. **Consolidate logging**:
   - Remove `utils/logging.py`
   - Update all imports to use `monitoring/logging.py`

8. **Add dependency injection**:
   - Make external dependencies injectable
   - Allow mocking in tests

9. **Standardize error handling**:
   - Create exception hierarchy
   - Use consistently across codebase

10. **Document test patterns** (`tests/README.md`):
    - Document how to write tests
    - Document fixtures available
    - Document mocking patterns

#### Phase 3: Reintroduce Heavier Checks (Days 11-21)

**Goal**: Add integration tests and security scans in a controlled way.

1. **Create nightly workflow** (`nightly.yml`):
   - Add integration test job
   - Add security scan job
   - Run on schedule

2. **Add integration tests** (`tests/integration/`):
   - Create integration test directory
   - Add tests that require real services
   - Mark with `@pytest.mark.integration`

3. **Fix security scans**:
   - Ensure `safety` and `bandit` are configured correctly
   - Fix or suppress false positives
   - Document security findings

4. **Add coverage reporting**:
   - Ensure codecov is configured
   - Set coverage thresholds (if desired)
   - Document coverage goals

5. **Add performance tests** (optional):
   - Mark slow tests
   - Add performance benchmarks

6. **Document CI process** (`CONTRIBUTING.md`):
   - Document what checks run when
   - Document how to run checks locally
   - Document how to fix common issues

### DEFINITION OF DONE FOR GREEN CI

**Success criteria:**

1. **All PRs to main run these checks and pass >95% of the time:**
   - `lint` (ruff + black)
   - `type-check` (mypy)
   - `test` (unit tests only, <5 min runtime)

2. **Flakiness is rare and tracked:**
   - Any flaky test is marked and documented
   - Flaky tests are fixed or moved to integration suite

3. **Local dev matches CI:**
   - `make ci` or `task ci` runs same checks as CI
   - Developers can reproduce CI failures locally

4. **Security scans run nightly:**
   - `safety` and `bandit` run on schedule
   - Findings are tracked and addressed

5. **Integration tests run nightly:**
   - Full test suite with real services
   - Catch integration issues before they hit main

---

## F. PR PLAN & LOCAL DEV PARITY

### PR PLAN

#### PR 1: Fix CI Workflow - Remove Duplication and Add Caching
**Title**: "ci: Consolidate workflows, add caching, fix security checks"  
**Scope**: CI workflow fixes only  
**Files**: `.github/workflows/ci.yml`  
**Risk**: Low  
**Dependencies**: None  
**Changes**:
- Remove duplicate linting from `test` job
- Add pip caching
- Fix security checks (remove `|| true`)
- Split into `lint`, `type-check`, `test`, `build` jobs
- Add pytest markers support

#### PR 2: Fix Test Infrastructure and Mocking
**Title**: "test: Add fixtures, markers, and mock external APIs"  
**Scope**: Test infrastructure improvements  
**Files**: `tests/conftest.py`, `pytest.ini`, `tests/test_agent.py`, `tests/utils.py`  
**Risk**: Medium  
**Dependencies**: PR 1 (for pytest markers)  
**Changes**:
- Create `conftest.py` with fixtures
- Create `pytest.ini` with markers
- Mock OpenAI API in `test_agent.py`
- Add test utilities
- Mark all tests with appropriate markers

#### PR 3: Fix Import-Time Side Effects and Logging Consolidation
**Title**: "refactor: Lazy initialization and consolidate logging"  
**Scope**: Code structure improvements  
**Files**: `agent_factory/api/main.py`, `agent_factory/utils/logging.py` (delete), imports  
**Risk**: Medium  
**Dependencies**: PR 2 (tests should pass)  
**Changes**:
- Move `init_db()` to startup event in FastAPI
- Remove `utils/logging.py`
- Update imports to use `monitoring/logging.py`
- Fix any import-time side effects

#### PR 4: Fix Type Annotations and Type Checking
**Title**: "types: Add missing type annotations and fix mypy errors"  
**Scope**: Type safety improvements  
**Files**: `agent_factory/core/*.py`, `agent_factory/api/*.py`, etc.  
**Risk**: Low  
**Dependencies**: PR 3  
**Changes**:
- Add return type annotations
- Fix generic types
- Add type stubs for missing dependencies
- Remove `--ignore-missing-imports` (or fix issues)

#### PR 5: Add Missing Test Coverage
**Title**: "test: Add tests for API routes, CLI, and database models"  
**Scope**: Test coverage expansion  
**Files**: `tests/test_api_*.py`, `tests/test_cli_*.py`, `tests/test_database_*.py`  
**Risk**: Low  
**Dependencies**: PR 2, PR 3  
**Changes**:
- Add tests for API routes (using FastAPI TestClient)
- Add tests for CLI commands
- Add tests for database models
- Increase overall coverage

#### PR 6: Create Nightly Workflow for Integration Tests
**Title**: "ci: Add nightly workflow for integration tests and security scans"  
**Scope**: CI workflow expansion  
**Files**: `.github/workflows/nightly.yml`  
**Risk**: Low  
**Dependencies**: PR 5 (integration tests should exist)  
**Changes**:
- Create `nightly.yml` workflow
- Add integration test job with PostgreSQL/Redis services
- Add security scan job
- Schedule to run nightly

### LOCAL DEV & CI PARITY

**Create `Makefile` or `taskfile.yml`:**

```makefile
# Makefile
.PHONY: ci lint type-check test test-unit test-integration format install

ci: lint type-check test-unit

lint:
	ruff check agent_factory/ tests/
	black --check agent_factory/ tests/

format:
	black agent_factory/ tests/
	ruff check --fix agent_factory/ tests/

type-check:
	mypy agent_factory/ --strict --no-ignore-missing-imports

test:
	pytest tests/ -v

test-unit:
	pytest tests/ -m "not integration and not slow" -v

test-integration:
	pytest tests/ -m integration -v

test-cov:
	pytest tests/ -m "not integration and not slow" -v --cov=agent_factory --cov-report=html

install:
	pip install -e ".[dev]"

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".ruff_cache" -exec rm -r {} +
```

**Or `taskfile.yml` (using Task):**

```yaml
version: '3'

tasks:
  ci:
    deps: [lint, type-check, test-unit]
    desc: Run all CI checks

  lint:
    desc: Run linters
    cmds:
      - ruff check agent_factory/ tests/
      - black --check agent_factory/ tests/

  format:
    desc: Format code
    cmds:
      - black agent_factory/ tests/
      - ruff check --fix agent_factory/ tests/

  type-check:
    desc: Run type checker
    cmds:
      - mypy agent_factory/ --strict --no-ignore-missing-imports

  test-unit:
    desc: Run unit tests
    cmds:
      - pytest tests/ -m "not integration and not slow" -v

  test-integration:
    desc: Run integration tests
    cmds:
      - pytest tests/ -m integration -v

  install:
    desc: Install dependencies
    cmds:
      - pip install -e ".[dev]"
```

**Document in `CONTRIBUTING.md`:**

```markdown
## Running CI Checks Locally

Before submitting a PR, run the same checks that CI runs:

```bash
# Using Make
make ci

# Or using Task
task ci

# Or manually
make lint
make type-check
make test-unit
```

## Test Markers

- `@pytest.mark.unit` - Fast unit tests (run in CI)
- `@pytest.mark.integration` - Integration tests (require services, run nightly)
- `@pytest.mark.slow` - Slow tests (>1s, run nightly)

Run specific test types:
```bash
pytest -m unit        # Unit tests only
pytest -m integration # Integration tests only
pytest -m "not slow" # Exclude slow tests
```
```

---

## G. 7-21 DAY ACTION CHECKLIST

### Week 1: Stop the Bleeding (Days 1-7)

**Day 1-2: CI Workflow Fixes**
- [QW] Remove `black --check` and `ruff check` from `test` job in `ci.yml`
- [QW] Remove `|| true` from security checks in `ci.yml`
- [QW] Add `cache: 'pip'` to Python setup actions in `ci.yml`
- [QW] Split `test` job into `lint`, `type-check`, `test`, `build` jobs
- [QW] Update `test` job to use `-m "not integration and not slow"` for pytest

**Day 3-4: Test Infrastructure**
- [DW] Create `tests/conftest.py` with fixtures for agents, tools, workflows
- [QW] Create `pytest.ini` with markers (`unit`, `integration`, `slow`)
- [DW] Mock OpenAI API calls in `tests/test_agent.py` using `unittest.mock`
- [QW] Mark all existing tests with `@pytest.mark.unit`
- [QW] Create `tests/utils.py` with helper functions for test data

**Day 5-7: Fix Import Issues**
- [DW] Move `init_db()` call to FastAPI startup event in `agent_factory/api/main.py`
- [QW] Remove `agent_factory/utils/logging.py` file
- [QW] Update imports from `utils.logging` to `monitoring.logging` (if any)
- [QW] Test that `agent_factory.api.main` can be imported without database

### Week 2: Core Fixes (Days 8-14)

**Day 8-9: Type Checking**
- [DW] Add return type annotations to all functions in `agent_factory/core/*.py`
- [DW] Fix generic types (e.g., `List` → `List[Agent]`)
- [QW] Create `py.typed` stub file if needed (already exists, verify)
- [DW] Gradually remove `--ignore-missing-imports` and fix type errors
- [QW] Add type stubs for external dependencies if needed

**Day 10-11: Linting**
- [QW] Run `black agent_factory/ tests/` to format all code
- [QW] Run `ruff check --fix agent_factory/ tests/` to auto-fix lint issues
- [DW] Manually fix any remaining lint errors
- [QW] Verify `make lint` passes locally

**Day 12-14: Test Coverage**
- [DW] Add tests for API routes (`tests/test_api_agents.py`, etc.)
- [DW] Add tests for CLI commands (`tests/test_cli_*.py`)
- [DW] Add tests for database models (`tests/test_database_models.py`)
- [QW] Ensure all new tests are marked with `@pytest.mark.unit` or `@pytest.mark.integration`

### Week 3: Polish & Nightly (Days 15-21)

**Day 15-16: Error Handling & Standards**
- [DW] Create `agent_factory/core/exceptions.py` with exception hierarchy
- [DW] Standardize error handling across core modules
- [QW] Add docstrings to any missing public APIs
- [QW] Review and fix any inconsistent naming

**Day 17-18: Integration Tests**
- [DW] Create `tests/integration/` directory
- [DW] Add integration tests for API with real database (in-memory SQLite)
- [DW] Add integration tests for workflows with mocked agents
- [QW] Mark all integration tests with `@pytest.mark.integration`

**Day 19-20: Nightly Workflow**
- [QW] Create `.github/workflows/nightly.yml`
- [QW] Add integration test job with PostgreSQL/Redis services
- [QW] Add security scan job (`safety`, `bandit`)
- [QW] Schedule workflow to run at 2 AM UTC daily

**Day 21: Documentation & Final Checks**
- [QW] Create `Makefile` or `taskfile.yml` for local CI parity
- [QW] Update `CONTRIBUTING.md` with local dev instructions
- [QW] Verify `make ci` runs same checks as GitHub Actions
- [QW] Test that PR workflow passes all checks
- [QW] Document any remaining flaky tests or known issues

---

## SUMMARY

**Immediate actions (this week):**
1. Fix CI workflow duplication and caching
2. Add test fixtures and mocking
3. Fix import-time side effects

**Short-term (next 2 weeks):**
4. Fix type annotations and linting
5. Add missing test coverage
6. Standardize error handling

**Long-term (week 3+):**
7. Add integration tests
8. Create nightly workflow
9. Document everything

**Success metrics:**
- ✅ PRs to main have <5 checks, all green >95% of the time
- ✅ Local `make ci` matches GitHub Actions exactly
- ✅ No flaky tests in main CI pipeline
- ✅ Integration tests run nightly and catch issues early

---

**Next Steps:**
1. Review this plan with the team
2. Start with PR 1 (CI workflow fixes)
3. Iterate through PRs 2-6 sequentially
4. Monitor CI health and adjust as needed
