# VS Code / Cursor IDE Configuration

This directory contains workspace settings for optimal Python development with Ruff linting.

## Setup Instructions

### 1. Install Required Extensions

When you open this workspace in Cursor/VS Code, you'll be prompted to install recommended extensions. Click "Install All" or install them manually:

**Required:**

- `charliermarsh.ruff` - Ruff linting and formatting
- `ms-python.python` - Python language support
- `ms-python.vscode-pylance` - Fast Python language server
- `ms-python.black-formatter` - Black code formatter

**Recommended:**

- `ms-toolsai.jupyter` - Jupyter notebook support
- `eamodio.gitlens` - Git integration
- `DavidAnson.vscode-markdownlint` - Markdown linting
- `yzhang.markdown-all-in-one` - Markdown editing features

### 2. Verify Python Interpreter

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Python: Select Interpreter"
3. Choose the `.venv` interpreter from this workspace

### 3. Configure Ruff

The workspace is already configured in `settings.json`. Ruff will:

- ✅ Lint your code on save
- ✅ Auto-fix issues when possible
- ✅ Organize imports automatically
- ✅ Show real-time errors and warnings

## What's Configured

### Linting

- **Ruff**: Enabled as primary linter (native extension)
- **Python Legacy Linting**: Disabled (Ruff extension handles everything)
- **Flake8/Pylint**: Not needed (Ruff replaces them)
- **Runs**: Automatically on file save with auto-fix

### Formatting

- **Black**: Python code formatting (88 char line length)
- **Format on Save**: Enabled for Python and Markdown
- **Import Organization**: Automatic via Ruff

### Markdown Linting

- **Markdownlint**: Enabled for all `.md` files
- **Rules**: Configured for documentation-friendly linting
- **Disabled Rules**:
  - MD013 (line length) - For flexibility with long links
  - MD033 (inline HTML) - Allows badges and formatting
  - MD041 (first line heading) - Not required in all docs

### Testing

- **Pytest**: Enabled and configured
- **Test Discovery**: Searches `lessons/` directory
- **Run Tests**: Click the flask icon in sidebar or use test explorer

## Manual Commands

You can also run these commands in the terminal:

```bash
# Lint all files
ruff check .

# Lint and auto-fix
ruff check . --fix

# Format with Black
black .

# Run tests
pytest

# Run tests with coverage
pytest --cov=lessons --cov-report=html
```

## Keyboard Shortcuts

### Cursor/VS Code

- `Cmd+S` / `Ctrl+S` - Save (triggers format and lint)
- `Cmd+Shift+P` / `Ctrl+Shift+P` - Command palette
- `Shift+Alt+F` - Format document manually
- `Cmd+.` / `Ctrl+.` - Quick fix (shows Ruff fixes)

### Running Tests

- Click the beaker/flask icon in the activity bar
- Or use the test explorer panel

## Troubleshooting

### "Legacy server (ruff-lsp) deprecated" warning

✅ **Fixed!** The settings now use the modern Ruff native extension.

- Old (deprecated): `ruff.lint.run`, separate linting config
- New (current): Native Ruff extension with `source.fixAll` in codeActionsOnSave

### IntelliCode/Pylance issues

✅ **Fixed!** Pylance is now re-enabled for IntelliSense.

- Pylance provides autocomplete, type checking, and IntelliCode
- Ruff provides linting and formatting
- They work together perfectly!

### Ruff not showing errors

1. Ensure the Ruff extension (`charliermarsh.ruff`) is installed
2. Check Output panel: `View > Output` and select "Ruff" from dropdown
3. Reload window: `Cmd+Shift+P` > "Developer: Reload Window"

### Python interpreter issues

1. Ensure virtual environment is activated: `source .venv/bin/activate`
2. Reinstall packages: `pip install -e ".[dev]"`
3. Select correct interpreter in Cursor/VS Code

### Format not working

1. Check that Black formatter extension is installed
2. Verify `python.formatting.provider` is set to "black" in settings
3. Try manual format: `Shift+Alt+F`

### Markdown linter issues

1. Ensure markdownlint extension (`DavidAnson.vscode-markdownlint`) is installed
2. Check `.markdownlint.json` in project root for rule configuration
3. Disable specific rules inline if needed: `<!-- markdownlint-disable MD001 -->`

## Additional Tips

### View Linter Output

- Open Output panel: `View > Output`
- Select "Ruff" from the dropdown
- See real-time linting results

### Ignore Specific Rules

Add inline comments when needed:

```python
from module import *  # noqa: F403
long_line_that_you_cant_break = "something"  # noqa: E501
```

### Configure Per File

Edit `.ruff.toml` or `pyproject.toml` for project-wide rules.

## Questions?

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for more development guidelines.
