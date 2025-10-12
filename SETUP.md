# Setup Guide

Quick start guide for getting the Python Learning Lab up and running.

## Prerequisites

- Python 3.9 or higher
- pip or pip3
- git (for cloning and version control)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ryfranklin/python-learning-lab.git
cd python-learning-lab
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e ".[dev]"
```

This installs the package in editable mode with all development dependencies including:
- pytest and pytest-asyncio
- black (code formatter)
- ruff (linter)
- bandit (security scanner)
- pre-commit (git hooks)
- jupyter and ipython

## Verify Installation

### Run Tests

```bash
pytest
```

All 60 tests should pass with 100% coverage.

### Run Demo

```bash
python examples/demo_event_bus.py
```

### Launch Jupyter

```bash
jupyter notebook notebooks/
```

## Optional: Pre-commit Hooks

Set up git hooks for automatic code quality checks:

```bash
pre-commit install
```

Now black, ruff, bandit, and pytest will run automatically on each commit.

## IDE Setup

### VS Code

Recommended extensions:
- Python
- Pylance
- Jupyter

Recommended settings (`.vscode/settings.json`):
```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.testing.pytestEnabled": true
}
```

### PyCharm

1. Set Python interpreter to `.venv/bin/python`
2. Enable pytest as test runner
3. Configure Black as external tool or use Black plugin

## Project Structure

```
python-learning-lab/
├── .github/workflows/      # CI/CD pipelines
├── core/                   # Shared utilities
├── lessons/                # All lab exercises
│   ├── lab_0001_event_bus/
│   ├── lab_0002_config_loader/
│   └── lab_0003_decorators/
├── examples/               # Demo scripts
├── notebooks/              # Jupyter notebooks
├── pyproject.toml         # Project configuration
└── README.md              # Main documentation
```

## Common Commands

### Testing

```bash
# Run all tests
pytest

# Run tests for specific lab
pytest lessons/lab_0001_event_bus/tests/

# Run with coverage
pytest --cov=lessons --cov-report=html

# Run specific test file
pytest lessons/lab_0001_event_bus/tests/test_sync_bus.py -v
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Fix linting issues automatically
ruff check --fix .

# Security scan
bandit -r lessons/ core/
```

### Development

```bash
# Install in editable mode
pip install -e .

# Update dependencies
pip install --upgrade -e ".[dev]"

# Freeze current environment
pip freeze > requirements-frozen.txt
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError: No module named 'lessons'`:

1. Ensure virtual environment is activated
2. Reinstall in editable mode: `pip install -e .`
3. Check that you're running from the project root

### Test Failures

If tests fail:

1. Ensure all dependencies are installed
2. Check Python version (3.9+)
3. Verify virtual environment is activated
4. Clear pytest cache: `rm -rf .pytest_cache`

### Jupyter Kernel Issues

If Jupyter can't find the correct kernel:

```bash
python -m ipykernel install --user --name=python-learning-lab
```

## Next Steps

1. Read the [main README](README.md)
2. Explore [Lab 0001: Event Bus](lessons/lab_0001_event_bus/README.md)
3. Run the demo: `python examples/demo_event_bus.py`
4. Try the Jupyter notebook: `notebooks/Lab_0001_EventBus.ipynb`
5. Check out [CONTRIBUTING.md](CONTRIBUTING.md) to add your own labs!

## Getting Help

- Check the [README](README.md) for project overview
- Read individual lab READMEs for specific topics
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub for bugs or questions

---

Happy Learning! 🚀

