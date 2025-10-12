# Removing Flake8 and Using Ruff

If you're seeing Flake8 warnings (like "line too long > 79 characters"), follow these steps to completely remove Flake8 and use Ruff instead.

## ✅ Ruff is Configured Correctly

Your project is already configured for:

- **Line length: 88 characters** (not 79)
- **E501 (line too long) is ignored** - Black handles this
- **Ruff replaces Flake8** completely

## 🔧 Steps to Remove Flake8 from IDE

### 1. Reload Cursor/VS Code Window

**This is the most important step!**

``` bash
Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows/Linux)
→ Type: "Developer: Reload Window"
→ Press Enter
```

### 2. Verify Extension Status

Check which extensions are installed:

1. Open Extensions panel (Cmd+Shift+X or Ctrl+Shift+X)
2. Search for "flake8"
3. If you see any Flake8-related extensions, **Uninstall** or **Disable** them:
   - `ms-python.flake8` (if exists)
   - Any other flake8 extensions

**Keep these extensions:**

- ✅ `charliermarsh.ruff` - Your new linter
- ✅ `ms-python.python` - Python support
- ✅ `ms-python.black-formatter` - Formatter
- ✅ `ms-python.vscode-pylance` - IntelliSense

### 3. Check for User-Level Settings Override

Your **User Settings** might be overriding workspace settings:

1. Open Settings: `Cmd+,` (or `Ctrl+,`)
2. Click the "User" tab (not "Workspace")
3. Search for: `python.linting.flake8`
4. If you see it enabled, **uncheck** it or set to `false`
5. Search for: `python.linting.enabled`
6. Make sure it's **not** forcing linting on

### 4. Clear Python Extension Cache

Sometimes the Python extension caches linter settings:

#### Option A: Command Palette

``` bash
Cmd+Shift+P → "Python: Clear Cache and Reload Window"
```

#### Option B: Manual

```bash
# Close Cursor/VS Code completely
# Then run:
rm -rf ~/Library/Caches/com.cursor.*
# or for VS Code:
rm -rf ~/Library/Application\ Support/Code/CachedData/
```

### 5. Verify Ruff is Working

Open any Python file and:

1. **Check the status bar** (bottom of window):
   - Should show "Ruff" when you have a Python file open
   - Click it to see Ruff output

2. **Make a test error:**

   ```python
   import os  # unused import
   x = [1, 2, 3]
   ```

   - You should see Ruff warnings (not Flake8)
   - Hover over the error - it should say "Ruff"

3. **Check Output panel:**
   - View → Output
   - Select "Ruff" from dropdown
   - Should see Ruff running, not Flake8

## 🎯 Confirming It's Fixed

### What You SHOULD See

- ✅ Line length errors at 88+ characters (not 79)
- ✅ Warnings say "Ruff" when you hover
- ✅ Output panel shows "Ruff" activity

### What You Should NOT See

- ❌ Warnings about > 79 characters
- ❌ Warnings saying "Flake8"
- ❌ Flake8 in Output panel dropdown

## 🐛 Still Seeing Flake8?

### Nuclear Option: Reset All Python Settings

1. **Open Settings JSON:**

   ``` bash
   Cmd+Shift+P → "Preferences: Open User Settings (JSON)"
   ```

2. **Remove all Flake8-related lines:**

   ```json
   // DELETE these if you find them:
   "python.linting.flake8Enabled": ...,
   "python.linting.flake8Path": ...,
   "python.linting.flake8Args": ...,
   ```

3. **Save and reload window**

### Check Python Extension Output

1. View → Output
2. Select "Python" from dropdown
3. Look for lines mentioning "flake8"
4. If you see it loading flake8, the settings haven't taken effect

## 📋 Current Configuration Summary

From `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88  # ✅ Not 79!

[tool.ruff.lint]
ignore = [
    "E501",  # line too long (handled by black)
]
```

From `.vscode/settings.json`:

```json
{
  "python.linting.enabled": false,         // ✅ Legacy linting OFF
  "python.linting.flake8Enabled": false,   // ✅ Flake8 explicitly OFF
  "ruff.enable": true,                     // ✅ Ruff ON
}
```

## ✅ Expected Behavior After Fix

When you open a Python file:

1. Ruff shows up in status bar
2. Line length warnings appear at 88+ chars (not 79)
3. Hover over warnings shows "Ruff: E..."
4. Auto-fix works with Cmd+. (Quick Fix)

## 🆘 Need More Help?

If you're still seeing Flake8 after all these steps:

1. Check which process is running:

   ```bash
   ps aux | grep flake8
   ```

2. Take a screenshot of:
   - The error message
   - Output panel (showing what's selected)
   - Extensions panel (showing installed extensions)

The issue is likely:

- Flake8 extension still installed
- User-level settings overriding workspace
- Window not reloaded after changes
