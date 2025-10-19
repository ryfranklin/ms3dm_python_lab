"""TOML configuration loader."""

import tomllib
from typing import Any

from .base_loader import BaseLoader


class TomlLoader(BaseLoader):
    """Configuration loader for TOML files."""

    def load(self) -> dict[str, Any]:
        """Load configuration from TOML file.

        Returns:
            Dictionary containing the configuration data

        Raises:
            ValueError: If the TOML format is invalid
            IOError: If there's an error reading the file
        """
        try:
            with open(self.file_path, "rb") as file:
                data = tomllib.load(file)

            if not isinstance(data, dict):
                raise ValueError(
                    f"TOML file must contain a dictionary, got {type(data)}"
                )

            return data

        except tomllib.TOMLDecodeError as e:
            raise ValueError(
                f"Invalid TOML format in {self.file_path}: {e}"
            ) from e
        except OSError as e:
            raise OSError(
                f"Error reading TOML file {self.file_path}: {e}"
            ) from e

    def get_supported_extensions(self) -> list[str]:
        """Get list of supported file extensions.

        Returns:
            List of supported TOML file extensions
        """
        return [".toml"]
