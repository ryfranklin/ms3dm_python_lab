"""Tests for the configuration manager."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml
from pydantic import BaseModel, ValidationError

from ..config_loader.config_manager import ConfigManager


class TestConfig(BaseModel):
    """Test Pydantic model for validation."""

    database_url: str
    api_timeout: int = 30
    debug: bool = False


class TestConfigManager:
    """Test cases for ConfigManager."""

    def test_init_with_data(self):
        """Test initialization with configuration data."""
        config_data = {"database": {"url": "postgresql://localhost:5432/test"}}
        manager = ConfigManager(config_data)
        assert manager.to_dict() == config_data

    def test_init_without_data(self):
        """Test initialization without configuration data."""
        manager = ConfigManager()
        assert manager.to_dict() == {}

    def test_load_from_json_file(self):
        """Test loading configuration from JSON file."""
        test_data = {
            "database": {"url": "postgresql://localhost:5432/test"},
            "api": {"timeout": 30},
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(test_data, f)
            f.flush()

            manager = ConfigManager.load_from_file(f.name)
            assert manager.to_dict() == test_data

            # Clean up
            Path(f.name).unlink()

    def test_load_from_yaml_file(self):
        """Test loading configuration from YAML file."""
        test_data = {
            "database": {"url": "postgresql://localhost:5432/test"},
            "api": {"timeout": 30},
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            yaml.dump(test_data, f)
            f.flush()

            manager = ConfigManager.load_from_file(f.name)
            assert manager.to_dict() == test_data

            # Clean up
            Path(f.name).unlink()

    def test_load_from_unsupported_file(self):
        """Test loading from unsupported file format raises ValueError."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"test content")
            f.flush()

            with pytest.raises(ValueError, match="Unsupported file format"):
                ConfigManager.load_from_file(f.name)

            # Clean up
            Path(f.name).unlink()

    def test_load_from_nonexistent_file(self):
        """Test loading from nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            ConfigManager.load_from_file("nonexistent.json")

    def test_get_with_dot_notation(self):
        """Test getting values using dot notation."""
        config_data = {
            "database": {
                "url": "postgresql://localhost:5432/test",
                "port": 5432,
            },
            "api": {"timeout": 30},
        }
        manager = ConfigManager(config_data)

        assert (
            manager.get("database.url") == "postgresql://localhost:5432/test"
        )
        assert manager.get("database.port") == 5432
        assert manager.get("api.timeout") == 30
        assert manager.get("nonexistent.key") is None
        assert manager.get("nonexistent.key", "default") == "default"

    def test_set_with_dot_notation(self):
        """Test setting values using dot notation."""
        manager = ConfigManager()

        manager.set("database.url", "postgresql://localhost:5432/test")
        manager.set("database.port", 5432)
        manager.set("api.timeout", 30)

        assert (
            manager.get("database.url") == "postgresql://localhost:5432/test"
        )
        assert manager.get("database.port") == 5432
        assert manager.get("api.timeout") == 30

    def test_has_method(self):
        """Test checking if keys exist."""
        config_data = {"database": {"url": "postgresql://localhost:5432/test"}}
        manager = ConfigManager(config_data)

        assert manager.has("database.url") is True
        assert manager.has("database.port") is False
        assert manager.has("nonexistent.key") is False

    def test_validate_with_pydantic(self):
        """Test validation with Pydantic model."""
        config_data = {
            "database_url": "postgresql://localhost:5432/test",
            "api_timeout": 60,
            "debug": True,
        }
        manager = ConfigManager(config_data)

        validated = manager.validate(TestConfig)
        assert isinstance(validated, TestConfig)
        assert validated.database_url == "postgresql://localhost:5432/test"
        assert validated.api_timeout == 60
        assert validated.debug is True

    def test_validate_with_invalid_data(self):
        """Test validation with invalid data raises ValidationError."""
        config_data = {
            "database_url": "postgresql://localhost:5432/test",
            "api_timeout": "not_a_number",  # Invalid type
            "debug": "not_a_boolean",  # Invalid type
        }
        manager = ConfigManager(config_data)

        with pytest.raises(ValidationError):
            manager.validate(TestConfig)

    def test_get_validated(self):
        """Test getting validated configuration."""
        config_data = {"database_url": "postgresql://localhost:5432/test"}
        manager = ConfigManager(config_data)

        # Initially no validated config
        assert manager.get_validated() is None

        # After validation
        manager.validate(TestConfig)
        validated = manager.get_validated()
        assert isinstance(validated, TestConfig)

    def test_update_with_config_manager(self):
        """Test updating with another ConfigManager."""
        config1 = ConfigManager(
            {"database": {"url": "postgresql://localhost:5432/test"}}
        )
        config2 = ConfigManager({"api": {"timeout": 30}})

        config1.update(config2)

        assert (
            config1.get("database.url") == "postgresql://localhost:5432/test"
        )
        assert config1.get("api.timeout") == 30

    def test_update_with_dictionary(self):
        """Test updating with dictionary."""
        manager = ConfigManager(
            {"database": {"url": "postgresql://localhost:5432/test"}}
        )
        update_dict = {"api": {"timeout": 30}}

        manager.update(update_dict)

        assert (
            manager.get("database.url") == "postgresql://localhost:5432/test"
        )
        assert manager.get("api.timeout") == 30

    def test_deep_update(self):
        """Test deep update of nested dictionaries."""
        manager = ConfigManager(
            {
                "database": {
                    "url": "postgresql://localhost:5432/test",
                    "port": 5432,
                }
            }
        )

        update_dict = {
            "database": {
                "url": "postgresql://localhost:5432/updated",  # Override
                "ssl": True,  # Add new key
            },
            "api": {"timeout": 30},  # Add new section
        }

        manager.update(update_dict)

        assert (
            manager.get("database.url")
            == "postgresql://localhost:5432/updated"
        )
        assert manager.get("database.port") == 5432  # Preserved
        assert manager.get("database.ssl") is True  # Added
        assert manager.get("api.timeout") == 30  # Added

    def test_dictionary_style_access(self):
        """Test dictionary-style access methods."""
        config_data = {"database": {"url": "postgresql://localhost:5432/test"}}
        manager = ConfigManager(config_data)

        # __getitem__
        assert manager["database"]["url"] == "postgresql://localhost:5432/test"

        # __setitem__
        manager["api"] = {"timeout": 30}
        assert manager.get("api.timeout") == 30

        # __contains__
        assert "database" in manager
        assert "nonexistent" not in manager

    def test_dictionary_style_access_missing_key(self):
        """Test dictionary-style access with missing key raises KeyError."""
        manager = ConfigManager()

        with pytest.raises(KeyError):
            _ = manager["nonexistent.key"]

    def test_repr(self):
        """Test string representation."""
        config_data = {"database": {"url": "postgresql://localhost:5432/test"}}
        manager = ConfigManager(config_data)

        repr_str = repr(manager)
        assert "ConfigManager" in repr_str
        assert "database" in repr_str

    def test_load_from_env_file(self):
        """Test loading from .env file."""
        env_content = """DATABASE_URL=postgresql://localhost:5432/test
API_TIMEOUT=30
DEBUG=true
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write(env_content)
            f.flush()

            manager = ConfigManager.load_from_env_file(f.name)

            # Should contain all environment variables
            assert isinstance(manager.to_dict(), dict)

            # Clean up
            Path(f.name).unlink()

    def test_load_from_env_file_specific_vars(self):
        """Test loading specific variables from .env file."""
        env_content = """DATABASE_URL=postgresql://localhost:5432/test
API_TIMEOUT=30
DEBUG=true
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write(env_content)
            f.flush()

            manager = ConfigManager.load_from_env_file(
                f.name, var_names=["DATABASE_URL", "API_TIMEOUT"]
            )

            result = manager.to_dict()
            assert "DATABASE_URL" in result
            assert "API_TIMEOUT" in result
            assert "DEBUG" not in result

            # Clean up
            Path(f.name).unlink()

    def test_load_with_validation(self):
        """Test loading file with immediate validation."""
        test_data = {
            "database_url": "postgresql://localhost:5432/test",
            "api_timeout": 60,
            "debug": True,
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(test_data, f)
            f.flush()

            manager = ConfigManager.load_from_file(
                f.name, validate_with=TestConfig
            )

            validated = manager.get_validated()
            assert isinstance(validated, TestConfig)
            assert validated.database_url == "postgresql://localhost:5432/test"

            # Clean up
            Path(f.name).unlink()
