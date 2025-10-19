"""Tests for the base loader."""

import tempfile
from pathlib import Path

import pytest

from ..config_loader.base_loader import BaseLoader


class ConcreteLoader(BaseLoader):
    """Concrete implementation of BaseLoader for testing."""

    def load(self):
        """Mock load implementation."""
        return {"test": "data"}

    def get_supported_extensions(self):
        """Mock extensions implementation."""
        return [".test"]


class TestBaseLoader:
    """Test cases for BaseLoader."""

    def test_init_with_existing_file(self):
        """Test initialization with existing file."""
        with tempfile.NamedTemporaryFile(suffix=".test", delete=False) as f:
            f.write(b"test content")
            f.flush()

            loader = ConcreteLoader(f.name)
            assert loader.file_path == Path(f.name)

            # Clean up
            Path(f.name).unlink()

    def test_init_with_nonexistent_file(self):
        """Test initialization with nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            ConcreteLoader("nonexistent.test")

    def test_init_with_directory(self):
        """Test initialization with directory raises ValueError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(ValueError, match="Path is not a file"):
                ConcreteLoader(temp_dir)

    def test_init_with_empty_file(self):
        """Test initialization with empty file raises ValueError."""
        with tempfile.NamedTemporaryFile(suffix=".test", delete=False) as f:
            f.write(b"")  # Empty file
            f.flush()

            with pytest.raises(
                ValueError, match="Configuration file is empty"
            ):
                ConcreteLoader(f.name)

            # Clean up
            Path(f.name).unlink()

    def test_load_method(self):
        """Test that load method returns expected data."""
        with tempfile.NamedTemporaryFile(suffix=".test", delete=False) as f:
            f.write(b"test content")
            f.flush()

            loader = ConcreteLoader(f.name)
            result = loader.load()
            assert result == {"test": "data"}

            # Clean up
            Path(f.name).unlink()

    def test_get_supported_extensions(self):
        """Test that get_supported_extensions returns expected extensions."""
        with tempfile.NamedTemporaryFile(suffix=".test", delete=False) as f:
            f.write(b"test content")
            f.flush()

            loader = ConcreteLoader(f.name)
            extensions = loader.get_supported_extensions()
            assert extensions == [".test"]

            # Clean up
            Path(f.name).unlink()

    def test_repr(self):
        """Test string representation."""
        with tempfile.NamedTemporaryFile(suffix=".test", delete=False) as f:
            f.write(b"test content")
            f.flush()

            loader = ConcreteLoader(f.name)
            repr_str = repr(loader)
            assert "ConcreteLoader" in repr_str
            assert f"file_path='{f.name}'" in repr_str

            # Clean up
            Path(f.name).unlink()
