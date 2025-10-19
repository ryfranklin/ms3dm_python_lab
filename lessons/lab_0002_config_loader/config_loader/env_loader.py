"""Environment variable configuration loader."""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from .base_loader import BaseLoader


class EnvLoader(BaseLoader):
    """Configuration loader for .env files."""

    def __init__(self, file_path: str | Path, override: bool = False):
        """Initialize the .env loader.

        Args:
            file_path: Path to the .env file
            override: Whether to override existing environment variables
        """
        super().__init__(file_path)
        self.override = override

    def load(self) -> dict[str, Any]:
        """Load configuration from .env file.

        Returns:
            Dictionary containing the environment variables

        Raises:
            ValueError: If there's an error loading the .env file
        """
        try:
            # Load .env file into environment variables
            load_dotenv(self.file_path, override=self.override)

            # Read all environment variables
            env_vars = dict(os.environ)

            # Filter out system variables if needed (optional)
            # For now, we'll return all environment variables
            return env_vars

        except Exception as e:
            raise ValueError(f"Error loading .env file {self.file_path}: {e}")

    def get_supported_extensions(self) -> list[str]:
        """Get list of supported file extensions.

        Returns:
            List of supported .env file extensions
        """
        return [".env"]

    def load_specific_vars(self, var_names: list[str]) -> dict[str, Any]:
        """Load only specific environment variables.

        Args:
            var_names: List of environment variable names to load

        Returns:
            Dictionary containing only the specified environment variables
        """
        try:
            load_dotenv(self.file_path, override=self.override)

            result = {}
            for var_name in var_names:
                value = os.getenv(var_name)
                if value is not None:
                    result[var_name] = value

            return result

        except Exception as e:
            raise ValueError(
                f"Error loading specific variables from .env file {self.file_path}: {e}"
            )
