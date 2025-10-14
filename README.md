# 🧪 Python Learning Lab

A structured learning environment for mastering Python concepts, patterns, and best practices. Each lab is a self-contained mini-project with production-ready code, comprehensive tests, and educational content.

## 🎯 Philosophy

This repository treats learning as **laboratory work** — hands-on, experimental, and rigorous. Each lab includes:

- **🧩 Implementation**: Production-quality code with proper documentation
- **🧪 Tests**: Comprehensive test coverage with pytest
- **📖 Learning Materials**: READMEs, notebooks, and examples
- **🛡️ Quality Assurance**: Linting, formatting, and security checks

## 📚 Labs

### Lab 0001: Event Bus

**Status**: ✅ Complete
**Concepts**: Observer Pattern, Pub/Sub, Async/Await, Decorators
**Location**: `lessons/lab_0001_event_bus/`

A lightweight publish/subscribe system with both synchronous and asynchronous implementations. Learn about decoupling components, defensive programming with assertions, and testing async code.

[View Lab 0001 →](lessons/lab_0001_event_bus/README.md)

### Lab 0002: Config Loader

**Status**: 🚧 Coming Soon
**Concepts**: File I/O, Data Validation, Type Hints
**Location**: `lessons/lab_0002_config_loader/`

### Lab 0003: Decorators

**Status**: 🚧 Coming Soon
**Concepts**: Higher-Order Functions, Closures, Metaprogramming
**Location**: `lessons/lab_0003_decorators/`

## 🚀 Getting Started

### Prerequisites

#### Option 1: Local Development

- Python 3.13 or higher
- pip for package management

#### Option 2: Docker (Recommended)

- Docker and Docker Compose
- No Python installation required!

### Installation

#### Using Docker (Recommended)

Docker provides a consistent environment across all machines and matches the CI/CD pipeline exactly.

1. **Clone the repository**

   ```bash
   git clone https://github.com/ryfranklin/python-learning-lab.git
   cd python-learning-lab
   ```

2. **Build the Docker image**

   ```bash
   make docker-build
   ```

3. **Run tests to verify setup**

   ```bash
   make docker-test
   ```

4. **Open a development shell** (optional)

   ```bash
   make docker-shell
   ```

#### Local Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ryfranklin/python-learning-lab.git
   cd python-learning-lab
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

4. **Set up pre-commit hooks** (optional but recommended)

   ```bash
   pre-commit install
   ```

### Running Tests

**Using Docker:**

```bash
# Run all tests
make docker-test

# Run tests with HTML coverage report
make docker-test-html

# Run all CI checks (tests + linting + type checking + security)
make docker-ci
```

**Using Local Environment:**

```bash
# Run all tests
pytest

# Run tests for a specific lab
pytest lessons/lab_0001_event_bus/tests/

# Run with coverage
pytest --cov=lessons --cov-report=html

# Run all CI checks
make ci
```

### Code Quality

**Using Docker:**

```bash
# Run linting
make docker-lint

# Format code
docker-compose run --rm format

# Run security scan
docker-compose run --rm security
```

**Using Local Environment:**

```bash
# Format code with Black and Ruff
make format

# Lint with Ruff
make lint

# Fix linting issues automatically
make lint-fix

# Type checking with Pyright
make typecheck

# Security scan with Bandit
make security
```

### Quick Commands

Use the Makefile for convenient commands:

```bash
# Show all available commands
make help

# Run everything before committing
make ci              # Local
make docker-ci       # Docker
```

## 🗂️ Repository Structure

```text
python-learning-lab/
├── pyproject.toml              # Project configuration and dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore patterns
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
│
├── core/                       # Shared utilities across all labs
│   ├── __init__.py
│   └── helpers.py
│
├── lessons/                    # All lab exercises
│   ├── lab_0001_event_bus/
│   │   ├── event_bus/         # Implementation
│   │   ├── tests/             # Test suite
│   │   └── README.md          # Lab documentation
│   │
│   ├── lab_0002_config_loader/
│   └── lab_0003_decorators/
│
├── examples/                   # Standalone demo scripts
│   └── demo_event_bus.py
│
└── notebooks/                  # Jupyter notebooks for exploration
    └── Lab_0001_EventBus.ipynb
```

## 🔄 CI/CD Pipeline

This project includes a comprehensive CI/CD pipeline that runs automatically on GitHub Actions and can be executed locally or in Docker.

### Automated Checks

Every push to `main` or `develop` branches and every pull request triggers:

#### 1. **Ruff Linting** 🧹

- **What it does:** Checks code style, unused imports, code complexity, and common errors
- **Rules enforced:** pycodestyle, pyflakes, isort, and flake8 extensions
- **Configuration:** `[tool.ruff]` in `pyproject.toml`
- **Run locally:** `make lint`

#### 2. **Pyright Type Checking** 🔍

- **What it does:** Validates type hints and catches type-related bugs before runtime
- **Mode:** Standard (balanced between strictness and usability)
- **Benefits:** Fewer runtime errors, better IDE support, clearer code
- **Configuration:** `[tool.pyright]` in `pyproject.toml`
- **Run locally:** `make typecheck`

#### 3. **Bandit Security Scanning** 🔒

- **What it does:** Identifies common security issues and vulnerabilities
- **Checks for:** SQL injection risks, unsafe YAML loading, weak cryptography, hardcoded passwords
- **Exclusions:** Test files (educational assertions are safe in tests)
- **Configuration:** `[tool.bandit]` in `pyproject.toml`
- **Run locally:** `make security`

#### 4. **Pytest Test Suite** ✅

- **What it does:** Runs all unit tests with coverage reporting
- **Coverage goal:** 100% for lesson code
- **Features:** Parallel execution, detailed failure reports, HTML coverage reports
- **Configuration:** `[tool.pytest.ini_options]` in `pyproject.toml`
- **Run locally:** `make test`

#### 5. **Docker Build Verification** 🐳

- **What it does:** Ensures the Docker image builds successfully
- **Multi-stage builds:** Base, dependencies, development, testing, linting
- **Benefits:** Consistent environment across all machines and CI/CD
- **Run locally:** `make docker-build`

### Pipeline Status

All checks must pass (green ✅) before merging. You can see the status:

- In GitHub pull requests
- On the Actions tab
- In commit status badges

### Running Locally

**Before committing:**

```bash
# Run all checks locally
make ci

# Or run the exact same checks as CI using Docker
make docker-ci
```

**Individual checks:**

```bash
make lint        # Ruff linting
make typecheck   # Pyright type checking
make security    # Bandit security scan
make test        # Pytest with coverage
```

### Docker Benefits

Using Docker ensures:

- ✅ **Consistency:** Same environment as CI/CD
- ✅ **Isolation:** No conflicts with local Python installations
- ✅ **Reproducibility:** Same results on all machines
- ✅ **Easy onboarding:** No complex local setup required

### Coverage Reports

Generate detailed coverage reports:

```bash
# HTML report (opens in browser) - Local
make test-html

# HTML report (opens in browser) - Docker
make docker-test-html

# Coverage badge
make coverage-badge
```

For more details, see [CI_CD_GUIDE.md](CI_CD_GUIDE.md).

## 🤝 Contributing

Want to add a new lab or improve an existing one? Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📖 Learning Path

Recommended order for working through the labs:

1. **Lab 0001: Event Bus** - Foundation in design patterns and async programming
2. **Lab 0002: Config Loader** - Data handling and validation
3. **Lab 0003: Decorators** - Advanced Python metaprogramming

Each lab builds on concepts from previous ones while remaining self-contained.

## 🛡️ Security

This repository follows security best practices:

- ✅ **Automated Security Scanning:** Bandit runs on every commit
- ✅ **Type Safety:** Pyright catches bugs before runtime
- ✅ **Dependency Management:** Pinned versions in `pyproject.toml`
- ✅ **Code Quality:** Ruff enforces best practices
- ✅ **CI/CD Pipeline:** All checks must pass before merging
- ✅ **Pre-commit Hooks:** Optional local validation
- ✅ **No Secrets:** All credentials excluded from version control

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

Built as a practical learning resource for Python developers at all levels. Inspired by production-ready code practices and test-driven development principles.

---

Happy Learning! 🚀
