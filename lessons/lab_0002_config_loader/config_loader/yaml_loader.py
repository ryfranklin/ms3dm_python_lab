"""YAML configuration loader."""

from typing import Any

import yaml

from .base_loader import BaseLoader


class YamlLoader(BaseLoader):
    """Configuration loader for YAML files."""

    def load(self) -> dict[str, Any]:
        """Load configuration from YAML file.

        Returns:
            Dictionary containing the configuration data

        Raises:
            ValueError: If the YAML format is invalid
            IOError: If there's an error reading the file
        """
        try:
            with open(self.file_path, encoding="utf-8") as file:
                data = yaml.safe_load(file)

            if data is None:
                return {}

            if not isinstance(data, dict):
                raise ValueError(
                    f"YAML file must contain a dictionary, got {type(data)}"
                )

            return data

        except yaml.YAMLError as e:
            raise ValueError(
                f"Invalid YAML format in {self.file_path}: {e}"
            ) from e
        except OSError as e:
            raise OSError(
                f"Error reading YAML file {self.file_path}: {e}"
            ) from e

    def get_supported_extensions(self) -> list[str]:
        """Get list of supported file extensions.

        Returns:
            List of supported YAML file extensions
        """
        return [".yaml", ".yml"]
