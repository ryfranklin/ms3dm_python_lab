"""Tests for the TOML loader."""

import tempfile
from pathlib import Path

import pytest
import tomli_w

from ..config_loader.toml_loader import TomlLoader


class TestTomlLoader:
    """Test cases for TomlLoader."""

    def test_load_valid_toml(self):
        """Test loading valid TOML file."""
        test_data = {
            "database": {"host": "localhost", "port": 5432},
            "api": {"timeout": 30},
        }

        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".toml", delete=False
        ) as f:
            tomli_w.dump(test_data, f)
            f.flush()

            loader = TomlLoader(f.name)
            result = loader.load()
            assert result == test_data

            # Clean up
            Path(f.name).unlink()

    def test_load_invalid_toml(self):
        """Test loading invalid TOML file raises ValueError."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False
        ) as f:
            f.write("invalid = toml = content [")  # Invalid TOML
            f.flush()

            loader = TomlLoader(f.name)
            with pytest.raises(ValueError, match="Invalid TOML format"):
                loader.load()

            # Clean up
            Path(f.name).unlink()

    def test_load_non_dict_toml(self):
        """Test loading TOML that's not a dictionary raises ValueError."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False
        ) as f:
            # Write a TOML file that when parsed returns a list (invalid for our loader)
            # We'll create a file that contains only an array
            f.write("[[array]]\n")
            f.write('item = "test"\n')
            f.flush()

            # Mock the tomllib.load to return a list instead of dict
            import tomllib

            original_load = tomllib.load

            def mock_load(file):
                return ["list", "not", "dict"]

            # Temporarily replace tomllib.load
            import tomllib

            tomllib.load = mock_load

            try:
                loader = TomlLoader(f.name)
                with pytest.raises(
                    ValueError, match="TOML file must contain a dictionary"
                ):
                    loader.load()
            finally:
                # Restore original tomllib.load
                tomllib.load = original_load

            # Clean up
            Path(f.name).unlink()

    def test_load_nonexistent_file(self):
        """Test loading nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            TomlLoader("nonexistent.toml")

    def test_get_supported_extensions(self):
        """Test that get_supported_extensions returns correct extensions."""
        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".toml", delete=False
        ) as f:
            tomli_w.dump({"test": "value"}, f)
            f.flush()

            loader = TomlLoader(f.name)
            extensions = loader.get_supported_extensions()
            assert extensions == [".toml"]

            # Clean up
            Path(f.name).unlink()

    def test_load_empty_toml_object(self):
        """Test loading empty TOML object."""
        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".toml", delete=False
        ) as f:
            tomli_w.dump({"empty": "object"}, f)
            f.flush()

            loader = TomlLoader(f.name)
            result = loader.load()
            assert result == {"empty": "object"}

            # Clean up
            Path(f.name).unlink()

    def test_load_nested_toml(self):
        """Test loading nested TOML structure."""
        test_data = {
            "level1": {"level2": {"level3": "deep_value"}},
            "array": [1, 2, 3],
            "boolean": True,
            "string_value": "test",
        }

        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".toml", delete=False
        ) as f:
            tomli_w.dump(test_data, f)
            f.flush()

            loader = TomlLoader(f.name)
            result = loader.load()
            assert result == test_data
            assert result["level1"]["level2"]["level3"] == "deep_value"
            assert result["array"] == [1, 2, 3]
            assert result["boolean"] is True
            assert result["string_value"] == "test"

            # Clean up
            Path(f.name).unlink()
