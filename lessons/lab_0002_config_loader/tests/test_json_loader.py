"""Tests for the JSON loader."""

import json
import tempfile
from pathlib import Path

import pytest

from ..config_loader.json_loader import JsonLoader


class TestJsonLoader:
    """Test cases for JsonLoader."""

    def test_load_valid_json(self):
        """Test loading valid JSON file."""
        test_data = {
            "database": {"host": "localhost", "port": 5432},
            "api": {"timeout": 30},
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(test_data, f)
            f.flush()

            loader = JsonLoader(f.name)
            result = loader.load()
            assert result == test_data

            # Clean up
            Path(f.name).unlink()

    def test_load_invalid_json(self):
        """Test loading invalid JSON file raises ValueError."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write('{"invalid": json}')  # Invalid JSON
            f.flush()

            loader = JsonLoader(f.name)
            with pytest.raises(ValueError, match="Invalid JSON format"):
                loader.load()

            # Clean up
            Path(f.name).unlink()

    def test_load_non_dict_json(self):
        """Test loading JSON that's not a dictionary raises ValueError."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(["list", "not", "dict"], f)
            f.flush()

            loader = JsonLoader(f.name)
            with pytest.raises(
                ValueError, match="JSON file must contain a dictionary"
            ):
                loader.load()

            # Clean up
            Path(f.name).unlink()

    def test_load_nonexistent_file(self):
        """Test loading nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            JsonLoader("nonexistent.json")

    def test_get_supported_extensions(self):
        """Test that get_supported_extensions returns correct extensions."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump({}, f)
            f.flush()

            loader = JsonLoader(f.name)
            extensions = loader.get_supported_extensions()
            assert extensions == [".json"]

            # Clean up
            Path(f.name).unlink()

    def test_load_empty_json_object(self):
        """Test loading empty JSON object."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump({}, f)
            f.flush()

            loader = JsonLoader(f.name)
            result = loader.load()
            assert result == {}

            # Clean up
            Path(f.name).unlink()

    def test_load_nested_json(self):
        """Test loading nested JSON structure."""
        test_data = {
            "level1": {"level2": {"level3": "deep_value"}},
            "array": [1, 2, 3],
            "boolean": True,
            "null_value": None,
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(test_data, f)
            f.flush()

            loader = JsonLoader(f.name)
            result = loader.load()
            assert result == test_data
            assert result["level1"]["level2"]["level3"] == "deep_value"
            assert result["array"] == [1, 2, 3]
            assert result["boolean"] is True
            assert result["null_value"] is None

            # Clean up
            Path(f.name).unlink()
