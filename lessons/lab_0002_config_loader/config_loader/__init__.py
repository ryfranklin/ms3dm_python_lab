"""Config Loader - A flexible configuration management system.

This module provides a comprehensive configuration loading system that supports
multiple file formats (JSON, YAML, TOML, .env) with validation using Pydantic.

Key Features:
- Strategy pattern for different file formats
- Pydantic models for validation and type safety
- Support for nested configurations
- Default values and fallbacks
- Environment variable overrides
- Comprehensive error handling

Example:
    from config_loader import ConfigManager

    # Load configuration from YAML file
    config = ConfigManager.load_from_file("config.yaml")

    # Access configuration values
    database_url = config.get("database.url")
    api_key = config.get("api.key", default="default-key")
"""

from .base_loader import BaseLoader
from .config_manager import ConfigManager
from .env_loader import EnvLoader
from .json_loader import JsonLoader
from .toml_loader import TomlLoader
from .yaml_loader import YamlLoader

__all__ = [
    "BaseLoader",
    "ConfigManager",
    "EnvLoader",
    "JsonLoader",
    "TomlLoader",
    "YamlLoader",
]

__version__ = "1.0.0"
