"""JSON configuration loader."""

import json
from typing import Any

from .base_loader import BaseLoader


class JsonLoader(BaseLoader):
    """Configuration loader for JSON files."""

    def load(self) -> dict[str, Any]:
        """Load configuration from JSON file.

        Returns:
            Dictionary containing the configuration data

        Raises:
            ValueError: If the JSON format is invalid
            IOError: If there's an error reading the file
        """
        try:
            with open(self.file_path, encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError(
                    f"JSON file must contain a dictionary, got {type(data)}"
                )

            return data

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON format in {self.file_path}: {e}"
            ) from e
        except OSError as e:
            raise OSError(
                f"Error reading JSON file {self.file_path}: {e}"
            ) from e

    def get_supported_extensions(self) -> list[str]:
        """Get list of supported file extensions.

        Returns:
            List of supported JSON file extensions
        """
        return [".json"]
