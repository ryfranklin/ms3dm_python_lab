"""Basic usage examples for the config loader."""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config_loader import ConfigManager

from core import get_logger, setup_logging

# Set up logging
setup_logging(level="INFO")
logger = get_logger(__name__)


def example_json_config():
    """Example using JSON configuration file."""
    logger.info("=== JSON Configuration Example ===")

    # Load from JSON file
    config = ConfigManager.load_from_file("examples/config.json")

    # Access values using dot notation
    database_url = config.get("database.url")
    api_timeout = config.get("api.timeout", default=30)

    logger.info(f"Database URL: {database_url}")
    logger.info(f"API Timeout: {api_timeout}")

    # Check if keys exist
    if config.has("database.ssl"):
        logger.info(f"SSL Enabled: {config.get('database.ssl')}")

    # Set new values
    config.set("debug", True)
    logger.info(f"Debug mode: {config.get('debug')}")


def example_yaml_config():
    """Example using YAML configuration file."""
    logger.info("\n=== YAML Configuration Example ===")

    # Load from YAML file
    config = ConfigManager.load_from_file("examples/config.yaml")

    # Access nested values
    redis_host = config.get("cache.redis.host")
    redis_port = config.get("cache.redis.port")

    logger.info(f"Redis Host: {redis_host}")
    logger.info(f"Redis Port: {redis_port}")

    # Access array values
    allowed_hosts = config.get("security.allowed_hosts", [])
    logger.info(f"Allowed Hosts: {allowed_hosts}")


def example_env_config():
    """Example using .env configuration file."""
    logger.info("\n=== Environment Configuration Example ===")

    # Load from .env file
    config = ConfigManager.load_from_env_file("examples/example.env")

    # Access environment variables
    database_url = config.get("DATABASE_URL")
    api_key = config.get("API_KEY")

    logger.info(f"Database URL: {database_url}")
    logger.info(
        f"API Key: {api_key[:10]}..." if api_key else "API Key: Not set"
    )


def example_validation():
    """Example using Pydantic validation."""
    logger.info("\n=== Pydantic Validation Example ===")

    from pydantic import BaseModel

    class DatabaseConfig(BaseModel):
        url: str
        port: int = 5432
        ssl: bool = False

    class AppConfig(BaseModel):
        database: DatabaseConfig
        debug: bool = False
        api_timeout: int = 30

    # Load and validate configuration
    config = ConfigManager.load_from_file("examples/config.json")

    try:
        validated_config = config.validate(AppConfig)
        logger.info("Configuration is valid!")
        logger.info(f"Database URL: {validated_config.database.url}")
        logger.info(f"Database Port: {validated_config.database.port}")
        logger.info(f"SSL Enabled: {validated_config.database.ssl}")
        logger.info(f"Debug Mode: {validated_config.debug}")
        logger.info(f"API Timeout: {validated_config.api_timeout}")
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")


def example_manual_config():
    """Example creating configuration manually."""
    logger.info("\n=== Manual Configuration Example ===")

    # Create configuration manually
    config = ConfigManager()

    # Set values using dot notation
    config.set("database.host", "localhost")
    config.set("database.port", 5432)
    config.set("database.name", "myapp")
    config.set("api.timeout", 30)
    config.set("api.retries", 3)

    # Access values
    logger.info(
        f"Database: {config.get('database.host')}:{config.get('database.port')}"
    )
    logger.info(f"Database Name: {config.get('database.name')}")
    logger.info(f"API Timeout: {config.get('api.timeout')} seconds")
    logger.info(f"API Retries: {config.get('api.retries')}")

    # Update with another configuration
    other_config = ConfigManager({"logging": {"level": "INFO"}})
    config.update(other_config)

    logger.info(f"Logging Level: {config.get('logging.level')}")


if __name__ == "__main__":
    # Run all examples
    example_manual_config()

    # These examples require the example config files to exist
    try:
        example_json_config()
    except FileNotFoundError:
        logger.warning("\nSkipping JSON example - config.json not found")

    try:
        example_yaml_config()
    except FileNotFoundError:
        logger.warning("\nSkipping YAML example - config.yaml not found")

    try:
        example_env_config()
    except FileNotFoundError:
        logger.warning("\nSkipping .env example - .env not found")

    try:
        example_validation()
    except FileNotFoundError:
        logger.warning("\nSkipping validation example - config.json not found")
