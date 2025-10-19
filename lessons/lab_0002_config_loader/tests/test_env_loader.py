"""Tests for the environment loader."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from ..config_loader.env_loader import EnvLoader


class TestEnvLoader:
    """Test cases for EnvLoader."""

    def test_load_env_file(self):
        """Test loading .env file."""
        env_content = """TEST_VAR=test_value
DATABASE_URL=postgresql://localhost:5432/test
API_KEY=secret_key_123
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write(env_content)
            f.flush()

            loader = EnvLoader(f.name)
            result = loader.load()

            # Should contain all environment variables (including system ones)
            assert isinstance(result, dict)
            assert "TEST_VAR" in result
            assert "DATABASE_URL" in result
            assert "API_KEY" in result

            # Clean up
            Path(f.name).unlink()

    def test_load_specific_vars(self):
        """Test loading specific environment variables."""
        env_content = """TEST_VAR=test_value
DATABASE_URL=postgresql://localhost:5432/test
API_KEY=secret_key_123
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write(env_content)
            f.flush()

            loader = EnvLoader(f.name)
            result = loader.load_specific_vars(
                ["TEST_VAR", "API_KEY", "NONEXISTENT"]
            )

            assert result == {
                "TEST_VAR": "test_value",
                "API_KEY": "secret_key_123",
            }

            # Clean up
            Path(f.name).unlink()

    def test_load_nonexistent_file(self):
        """Test loading nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            EnvLoader("nonexistent.env")

    def test_get_supported_extensions(self):
        """Test that get_supported_extensions returns correct extensions."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write("TEST=value")
            f.flush()

            loader = EnvLoader(f.name)
            extensions = loader.get_supported_extensions()
            assert extensions == [".env"]

            # Clean up
            Path(f.name).unlink()

    def test_override_parameter(self):
        """Test that override parameter is passed correctly."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write("TEST=value")
            f.flush()

            loader = EnvLoader(f.name, override=True)
            assert loader.override is True

            loader2 = EnvLoader(f.name, override=False)
            assert loader2.override is False

            # Clean up
            Path(f.name).unlink()

    def test_load_empty_env_file(self):
        """Test loading empty .env file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write("")  # Empty file
            f.flush()

            loader = EnvLoader(f.name)
            result = loader.load()

            # Should still return environment variables (system ones)
            assert isinstance(result, dict)

            # Clean up
            Path(f.name).unlink()

    def test_load_env_file_with_comments(self):
        """Test loading .env file with comments."""
        env_content = """# This is a comment
TEST_VAR=test_value
# Another comment
DATABASE_URL=postgresql://localhost:5432/test
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write(env_content)
            f.flush()

            loader = EnvLoader(f.name)
            result = loader.load()

            assert "TEST_VAR" in result
            assert "DATABASE_URL" in result

            # Clean up
            Path(f.name).unlink()

    def test_load_env_file_with_quotes(self):
        """Test loading .env file with quoted values."""
        env_content = """TEST_VAR="quoted value"
DATABASE_URL='postgresql://localhost:5432/test'
API_KEY="secret_key_123"
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write(env_content)
            f.flush()

            loader = EnvLoader(f.name)
            result = loader.load()

            assert "TEST_VAR" in result
            assert "DATABASE_URL" in result
            assert "API_KEY" in result

            # Clean up
            Path(f.name).unlink()

    @patch("os.environ", {})
    def test_load_with_empty_environment(self):
        """Test loading .env file when environment is empty."""
        env_content = """TEST_VAR=test_value
DATABASE_URL=postgresql://localhost:5432/test
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write(env_content)
            f.flush()

            loader = EnvLoader(f.name)
            result = loader.load()

            # Should only contain variables from .env file
            assert result == {
                "TEST_VAR": "test_value",
                "DATABASE_URL": "postgresql://localhost:5432/test",
            }

            # Clean up
            Path(f.name).unlink()
