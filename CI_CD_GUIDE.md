# CI/CD Pipeline Guide

## 🚀 Overview

Your Python Learning Lab now has a complete CI/CD pipeline with Docker support. This guide will help you use all the tools effectively.

## 📋 Quick Reference

### Local Commands (Makefile)

```bash
# Show all available commands
make help

# Run all CI checks locally
make ci

# Individual checks
make lint          # Run ruff linter
make typecheck     # Run pyright type checker
make security      # Run bandit security scan
make test          # Run pytest with coverage
make test-html     # Run tests with HTML coverage report

# Code formatting
make format        # Format with black and ruff

# Coverage visualization
make test-html     # Generate and open HTML coverage report
make coverage-badge # Generate coverage badge SVG

# Utilities
make clean         # Remove cache/build artifacts
make install       # Install dependencies
```

### Docker Commands

```bash
# Build Docker image
make docker-build

# Run checks in Docker
make docker-ci        # All checks
make docker-test      # Tests only
make docker-test-html # Tests with HTML coverage report
make docker-lint      # Linting only

# Development
make docker-shell  # Open bash in container

# Cleanup
make docker-clean  # Remove Docker resources
```

### Docker Compose (Alternative)

```bash
# Run individual services
docker-compose run --rm test      # Run tests
docker-compose run --rm test-html # Run tests with HTML coverage report
docker-compose run --rm lint      # Run linters
docker-compose run --rm ci        # Run all checks
docker-compose run --rm format    # Format code
docker-compose run --rm security  # Security scan
docker-compose run --rm typecheck # Type checking

# Development shell
docker-compose run --rm dev bash
```

## 🔧 What Each Tool Does

### **Ruff** - Fast Python Linter

- **What:** Checks code style and common errors
- **Config:** `[tool.ruff]` in `pyproject.toml`
- **Rules:** pycodestyle, pyflakes, isort, flake8 extensions

### **Pyright** - Static Type Checker

- **What:** Validates type hints at development time
- **Config:** `[tool.pyright]` in `pyproject.toml`
- **Mode:** `standard` (balanced strictness)
- **Integration:** Real-time checking in VS Code via Pylance

### **Bandit** - Security Scanner

- **What:** Finds common security issues
- **Config:** `[tool.bandit]` in `pyproject.toml`
- **Exclusions:** Tests (asserts are educational, not production)

### **Pytest** - Testing Framework

- **What:** Runs your test suite
- **Config:** `[tool.pytest.ini_options]` in `pyproject.toml`
- **Coverage:** Shows which lines are tested

### **Black** - Code Formatter

- **What:** Auto-formats Python code
- **Config:** `[tool.black]` in `pyproject.toml`
- **Line length:** 88 characters

## 🤖 GitHub Actions (Automated CI)

When you push to `main` or `develop`, GitHub automatically runs:

1. **Lint Job** - Runs ruff
2. **Type Check Job** - Runs pyright
3. **Security Job** - Runs bandit
4. **Test Job** - Runs pytest with coverage
5. **Docker Build** - Verifies Docker image builds
6. **All Checks Pass** - Final green checkmark

### Workflow File

- Location: `.github/workflows/ci.yml`
- Triggers: Push to `main`/`develop`, Pull Requests
- Runs on: Ubuntu (latest)
- Python version: 3.13

## 📦 Docker Setup

### Multi-Stage Dockerfile

```text
base        → Python 3.13 slim
dependencies → Install pip packages
development → Full dev environment
testing     → Optimized for tests
linting     → Optimized for checks
```

### Benefits

- ✅ Consistent environment across all machines
- ✅ Isolated from your local setup
- ✅ Same environment as CI/CD
- ✅ Easy onboarding for new developers

## 🎯 Development Workflow

### Before Committing

```bash
# Check your code
make ci

# Format if needed
make format

# Fix any issues
make lint-fix
```

### After Pushing

- Watch GitHub Actions (green checkmarks)
- Check coverage report in PR
- Review any failed checks

### In VS Code

- **Real-time type checking** - Red squiggles for type errors
- **Format on save** - Black formats automatically
- **Import sorting** - Ruff organizes imports

## 🔍 Troubleshooting

### "Tests fail locally but pass in Docker"

- Different Python version
- Missing dependencies
- Solution: Use `make docker-test` to match CI environment

### "Type errors in VS Code but pyright passes"

- VS Code cache issue
- Solution: Reload window (`Cmd+Shift+P` → "Reload Window")

### "Docker build is slow"

- First build is slow (downloads packages)
- Subsequent builds use cache
- Solution: Be patient on first run

### "make ci fails on security check"

- Bandit found potential issues
- Review the specific file and line
- If educational (assert), it's already excluded

## 📊 Coverage Reports

### Terminal Reports (Quick View)

After running tests:

```bash
make test
# Shows coverage in terminal
# Green = tested, Red = missing lines
```

### HTML Reports (Detailed Analysis)

Generate beautiful interactive HTML coverage reports:

```bash
# Local environment
make test-html

# Docker environment
make docker-test-html

# Both commands automatically open htmlcov/index.html in browser
```

**HTML Report Features:**

- 📈 Overall coverage percentage with visual bars
- 📁 File-by-file breakdown (clickable)
- 🔍 Line-by-line highlighting:
  - **Green lines** = tested
  - **Red lines** = not tested
  - **Yellow lines** = partially tested (branches)
- 📊 Missing lines listed for each file
- 🎯 Branch coverage visualization

### Coverage Badge

Generate a badge for your README:

```bash
make coverage-badge
# Creates coverage.svg
```

Then add to README.md:

```markdown
![Coverage](./coverage.svg)
```

### Coverage in This Project

- **Goal:** 100% for lesson code
- **Current:** 94% (helper functions not tested yet)
- **View Options:**
  - Terminal: `make test`
  - HTML: `make test-html`
  - Badge: `make coverage-badge`

## 🎓 Best Practices

1. **Run `make ci` before committing**
2. **Keep tests passing** - Green is good
3. **Fix type errors** - Pyright helps catch bugs
4. **Review security warnings** - Even "low" severity
5. **Maintain 100% coverage** - Test everything educational

## 📚 Next Steps

- **Add pre-commit hooks:** `make pre-commit-install`
- **Set up Codecov:** Add `CODECOV_TOKEN` to GitHub secrets
- **Deploy:** Add deployment steps to workflow
- **Badges:** Add CI status badges to README

## 🆘 Getting Help

- **Makefile:** `make help`
- **Docker:** `docker-compose --help`
- **GitHub Actions:** Check `.github/workflows/ci.yml`
- **Tool configs:** All in `pyproject.toml`

---

**Pro Tip:** Use `make docker-ci` to run the exact same checks as GitHub Actions before pushing!
