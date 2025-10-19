"""Main configuration manager with Pydantic validation."""

from pathlib import Path
from typing import Any, Union

from pydantic import BaseModel, ValidationError

from .base_loader import BaseLoader
from .env_loader import EnvLoader
from .json_loader import JsonLoader
from .toml_loader import TomlLoader
from .yaml_loader import YamlLoader


class ConfigManager:
    """Main configuration manager that orchestrates different loaders.

    This class provides a unified interface for loading configuration from
    different file formats with Pydantic validation support.
    """

    # Registry of available loaders
    _loaders: dict[str, type[BaseLoader]] = {
        ".json": JsonLoader,
        ".yaml": YamlLoader,
        ".yml": YamlLoader,
        ".toml": TomlLoader,
        ".env": EnvLoader,
    }

    def __init__(self, config_data: dict[str, Any] | None = None):
        """Initialize the configuration manager.

        Args:
            config_data: Optional initial configuration data
        """
        self._config: dict[str, Any] = config_data or {}
        self._validated_config: BaseModel | None = None

    @classmethod
    def load_from_file(
        cls,
        file_path: str | Path,
        validate_with: type[BaseModel] | None = None,
    ) -> "ConfigManager":
        """Load configuration from a file.

        Args:
            file_path: Path to the configuration file
            validate_with: Optional Pydantic model for validation

        Returns:
            ConfigManager instance with loaded configuration

        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        file_path = Path(file_path)
        file_extension = file_path.suffix.lower()

        if file_extension not in cls._loaders:
            supported = ", ".join(cls._loaders.keys())
            raise ValueError(
                f"Unsupported file format: {file_extension}. Supported: {supported}"
            )

        loader_class = cls._loaders[file_extension]
        loader = loader_class(file_path)
        config_data = loader.load()

        manager = cls(config_data)

        if validate_with:
            manager.validate(validate_with)

        return manager

    @classmethod
    def load_from_env_file(
        cls,
        file_path: str | Path,
        var_names: list[str] | None = None,
        validate_with: type[BaseModel] | None = None,
    ) -> "ConfigManager":
        """Load configuration from .env file.

        Args:
            file_path: Path to the .env file
            var_names: Optional list of specific variables to load
            validate_with: Optional Pydantic model for validation

        Returns:
            ConfigManager instance with loaded environment variables
        """
        loader = EnvLoader(file_path)

        if var_names:
            config_data = loader.load_specific_vars(var_names)
        else:
            config_data = loader.load()

        manager = cls(config_data)

        if validate_with:
            manager.validate(validate_with)

        return manager

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.

        Args:
            key: Configuration key (supports dot notation for nested keys)
            default: Default value if key is not found

        Returns:
            Configuration value or default

        Example:
            config.get("database.host")  # Gets config["database"]["host"]
            config.get("api.timeout", 30)  # Gets config["api"]["timeout"] or 30
        """
        keys = key.split(".")
        value = self._config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value using dot notation.

        Args:
            key: Configuration key (supports dot notation for nested keys)
            value: Value to set

        Example:
            config.set("database.host", "localhost")
            config.set("api.timeout", 30)
        """
        keys = key.split(".")
        current = self._config

        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        # Set the final value
        current[keys[-1]] = value

    def has(self, key: str) -> bool:
        """Check if a configuration key exists.

        Args:
            key: Configuration key (supports dot notation for nested keys)

        Returns:
            True if key exists, False otherwise
        """
        return self.get(key) is not None

    def validate(self, model_class: type[BaseModel]) -> BaseModel:
        """Validate configuration using a Pydantic model.

        Args:
            model_class: Pydantic model class for validation

        Returns:
            Validated configuration model

        Raises:
            ValidationError: If configuration doesn't match the model
        """
        try:
            validated = model_class(**self._config)
            self._validated_config = validated
            return validated
        except ValidationError as e:
            raise ValidationError(f"Configuration validation failed: {e}")

    def get_validated(self) -> BaseModel | None:
        """Get the validated configuration model.

        Returns:
            Validated configuration model or None if not validated
        """
        return self._validated_config

    def to_dict(self) -> dict[str, Any]:
        """Get the raw configuration as a dictionary.

        Returns:
            Configuration dictionary
        """
        return self._config.copy()

    def update(self, other: Union["ConfigManager", dict[str, Any]]) -> None:
        """Update configuration with another ConfigManager or dictionary.

        Args:
            other: ConfigManager instance or dictionary to merge
        """
        if isinstance(other, ConfigManager):
            other_dict = other.to_dict()
        else:
            other_dict = other

        self._deep_update(self._config, other_dict)

    def _deep_update(
        self, base_dict: dict[str, Any], update_dict: dict[str, Any]
    ) -> None:
        """Recursively update nested dictionaries.

        Args:
            base_dict: Base dictionary to update
            update_dict: Dictionary with updates
        """
        for key, value in update_dict.items():
            if (
                key in base_dict
                and isinstance(base_dict[key], dict)
                and isinstance(value, dict)
            ):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value

    def __getitem__(self, key: str) -> Any:
        """Get configuration value using dictionary-style access.

        Args:
            key: Configuration key

        Returns:
            Configuration value

        Raises:
            KeyError: If key is not found
        """
        value = self.get(key)
        if value is None:
            raise KeyError(f"Configuration key not found: {key}")
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        """Set configuration value using dictionary-style access.

        Args:
            key: Configuration key
            value: Value to set
        """
        self.set(key, value)

    def __contains__(self, key: str) -> bool:
        """Check if configuration key exists using 'in' operator.

        Args:
            key: Configuration key

        Returns:
            True if key exists, False otherwise
        """
        return self.has(key)

    def __repr__(self) -> str:
        """String representation of the configuration manager."""
        return f"ConfigManager(config_keys={list(self._config.keys())})"
