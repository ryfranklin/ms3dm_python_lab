"""Tests for the YAML loader."""

import tempfile
from pathlib import Path

import pytest
import yaml

from ..config_loader.yaml_loader import YamlLoader


class TestYamlLoader:
    """Test cases for YamlLoader."""

    def test_load_valid_yaml(self):
        """Test loading valid YAML file."""
        test_data = {
            "database": {"host": "localhost", "port": 5432},
            "api": {"timeout": 30},
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            yaml.dump(test_data, f)
            f.flush()

            loader = YamlLoader(f.name)
            result = loader.load()
            assert result == test_data

            # Clean up
            Path(f.name).unlink()

    def test_load_valid_yml_extension(self):
        """Test loading valid YAML file with .yml extension."""
        test_data = {"test": "data"}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yml", delete=False
        ) as f:
            yaml.dump(test_data, f)
            f.flush()

            loader = YamlLoader(f.name)
            result = loader.load()
            assert result == test_data

            # Clean up
            Path(f.name).unlink()

    def test_load_invalid_yaml(self):
        """Test loading invalid YAML file raises ValueError."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            f.write("invalid: yaml: content: [")  # Invalid YAML
            f.flush()

            loader = YamlLoader(f.name)
            with pytest.raises(ValueError, match="Invalid YAML format"):
                loader.load()

            # Clean up
            Path(f.name).unlink()

    def test_load_non_dict_yaml(self):
        """Test loading YAML that's not a dictionary raises ValueError."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            yaml.dump(["list", "not", "dict"], f)
            f.flush()

            loader = YamlLoader(f.name)
            with pytest.raises(
                ValueError, match="YAML file must contain a dictionary"
            ):
                loader.load()

            # Clean up
            Path(f.name).unlink()

    def test_load_empty_yaml(self):
        """Test loading empty YAML file returns empty dict."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            f.write("empty: value")  # Non-empty file
            f.flush()

            loader = YamlLoader(f.name)
            result = loader.load()
            assert result == {"empty": "value"}

            # Clean up
            Path(f.name).unlink()

    def test_load_none_yaml(self):
        """Test loading YAML with only comments returns empty dict."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            f.write("# This is just a comment\n# Another comment")
            f.flush()

            loader = YamlLoader(f.name)
            result = loader.load()
            assert result == {}

            # Clean up
            Path(f.name).unlink()

    def test_get_supported_extensions(self):
        """Test that get_supported_extensions returns correct extensions."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            yaml.dump({}, f)
            f.flush()

            loader = YamlLoader(f.name)
            extensions = loader.get_supported_extensions()
            assert extensions == [".yaml", ".yml"]

            # Clean up
            Path(f.name).unlink()

    def test_load_nested_yaml(self):
        """Test loading nested YAML structure."""
        test_data = {
            "level1": {"level2": {"level3": "deep_value"}},
            "array": [1, 2, 3],
            "boolean": True,
            "null_value": None,
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            yaml.dump(test_data, f)
            f.flush()

            loader = YamlLoader(f.name)
            result = loader.load()
            assert result == test_data
            assert result["level1"]["level2"]["level3"] == "deep_value"
            assert result["array"] == [1, 2, 3]
            assert result["boolean"] is True
            assert result["null_value"] is None

            # Clean up
            Path(f.name).unlink()
