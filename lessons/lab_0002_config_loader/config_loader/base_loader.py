"""Abstract base class for configuration loaders."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseLoader(ABC):
    """Abstract base class for configuration loaders.

    This class defines the interface that all configuration loaders must implement.
    It provides common functionality for file validation and error handling.
    """

    def __init__(self, file_path: str | Path):
        """Initialize the loader with a file path.

        Args:
            file_path: Path to the configuration file

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file path is invalid
        """
        self.file_path = Path(file_path)
        self._validate_file_path()

    def _validate_file_path(self) -> None:
        """Validate that the file path exists and is readable.

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file path is invalid
        """
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.file_path}"
            )

        if not self.file_path.is_file():
            raise ValueError(f"Path is not a file: {self.file_path}")

        if not self.file_path.stat().st_size > 0:
            raise ValueError(f"Configuration file is empty: {self.file_path}")

    @abstractmethod
    def load(self) -> dict[str, Any]:
        """Load configuration from the file.

        Returns:
            Dictionary containing the configuration data

        Raises:
            ValueError: If the file format is invalid
            IOError: If there's an error reading the file
        """
        pass

    @abstractmethod
    def get_supported_extensions(self) -> list[str]:
        """Get list of supported file extensions.

        Returns:
            List of supported file extensions (e.g., ['.json', '.yaml'])
        """
        pass

    def __repr__(self) -> str:
        """String representation of the loader."""
        return f"{self.__class__.__name__}(file_path='{self.file_path}')"
