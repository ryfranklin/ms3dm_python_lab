# Lab 0002: Config Loader

**Status**: ✅ Complete
**Difficulty**: Beginner to Intermediate
**Concepts**: File I/O, Data Validation, Type Hints, Design Patterns, Strategy Pattern

## 🎯 Learning Objectives

By the end of this lab, you will understand:

- ✅ How to load configuration from multiple file formats (JSON, YAML, TOML, .env)
- ✅ How to validate configuration data with Pydantic models
- ✅ How to implement the Strategy pattern for different loaders
- ✅ How to handle errors gracefully in file operations
- ✅ How to write comprehensive tests for file I/O operations
- ✅ How to use dot notation for nested configuration access

## 📚 What is a Config Loader?

A **Config Loader** is a system that manages application configuration from various sources. This lab provides a flexible, type-safe configuration management system that supports multiple file formats with validation.

Key features:

- **Multiple Format Support**: JSON, YAML, TOML, and .env files
- **Type Safety**: Pydantic validation for configuration data
- **Dot Notation**: Easy access to nested configuration values
- **Strategy Pattern**: Pluggable loaders for different file formats
- **Error Handling**: Comprehensive error handling and validation

## 🏗️ Architecture

This lab implements a flexible configuration system using several design patterns:

### 1. **Strategy Pattern** - File Format Loaders

Different loaders handle different file formats:

- `JsonLoader` - JSON files
- `YamlLoader` - YAML files
- `TomlLoader` - TOML files
- `EnvLoader` - Environment variable files

### 2. **Factory Pattern** - Loader Selection

The `ConfigManager` automatically selects the appropriate loader based on file extension.

### 3. **Validation** - Pydantic Integration

Configuration data can be validated using Pydantic models for type safety.

## 🚀 Quick Start

### Installation

```bash
# From the repository root
cd lessons/lab_0002_config_loader
```

### Basic Usage

```python
from config_loader import ConfigManager

# Load from JSON file
config = ConfigManager.load_from_file("config.json")

# Access values using dot notation
database_url = config.get("database.url")
api_timeout = config.get("api.timeout", default=30)

# Set new values
config.set("debug", True)

# Check if keys exist
if config.has("database.ssl"):
    ssl_enabled = config.get("database.ssl")
```

### Advanced Usage - Validation

```python
from pydantic import BaseModel
from config_loader import ConfigManager

class DatabaseConfig(BaseModel):
    url: str
    port: int = 5432
    ssl: bool = False

class AppConfig(BaseModel):
    database: DatabaseConfig
    debug: bool = False
    api_timeout: int = 30

# Load and validate configuration
config = ConfigManager.load_from_file("config.json")
validated_config = config.validate(AppConfig)

# Now you have type-safe access
print(f"Database: {validated_config.database.url}")
print(f"Port: {validated_config.database.port}")
```

## 🔍 Key Features

### 1. **Multiple File Format Support**

```python
# JSON
config = ConfigManager.load_from_file("config.json")

# YAML
config = ConfigManager.load_from_file("config.yaml")

# TOML
config = ConfigManager.load_from_file("config.toml")

# Environment variables
config = ConfigManager.load_from_env_file(".env")
```

### 2. **Dot Notation Access**

```python
# Access nested values easily
database_host = config.get("database.host")
redis_port = config.get("cache.redis.port")

# Set nested values
config.set("database.ssl", True)
config.set("api.timeout", 60)
```

### 3. **Environment Variable Overrides**

```python
# Load from .env file
config = ConfigManager.load_from_env_file(".env")

# Access environment variables
api_key = config.get("API_KEY")
database_url = config.get("DATABASE_URL")
```

### 4. **Pydantic Validation**

```python
from pydantic import BaseModel, Field

class Config(BaseModel):
    database_url: str = Field(..., description="Database connection URL")
    api_timeout: int = Field(default=30, ge=1, le=300)
    debug: bool = False

# Validate configuration
validated = config.validate(Config)
```

### 5. **Configuration Merging**

```python
# Merge configurations
config1 = ConfigManager({"database": {"host": "localhost"}})
config2 = ConfigManager({"api": {"timeout": 30}})

config1.update(config2)
# Now config1 contains both database and api settings
```

## 🧪 Running Tests

This lab includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/test_json_loader.py
pytest tests/test_yaml_loader.py
pytest tests/test_config_manager.py

# Run with coverage
pytest --cov=config_loader --cov-report=term-missing

# Run with verbose output
pytest -v
```

Test coverage includes:

- ✅ All file format loaders (JSON, YAML, TOML, .env)
- ✅ Configuration manager orchestration
- ✅ Pydantic validation
- ✅ Error handling and edge cases
- ✅ Dot notation access
- ✅ Configuration merging
- ✅ File I/O operations

## 💡 Examples

### Example 1: Basic Configuration

```python
from config_loader import ConfigManager

# Create configuration manually
config = ConfigManager()
config.set("database.host", "localhost")
config.set("database.port", 5432)
config.set("api.timeout", 30)

# Access values
print(f"Database: {config.get('database.host')}:{config.get('database.port')}")
```

### Example 2: Loading from File

```python
# Load from JSON file
config = ConfigManager.load_from_file("config.json")

# Access with defaults
timeout = config.get("api.timeout", default=30)
debug = config.get("debug", default=False)
```

### Example 3: Environment Variables

```python
# Load specific environment variables
config = ConfigManager.load_from_env_file(
    ".env",
    var_names=["DATABASE_URL", "API_KEY"]
)

database_url = config.get("DATABASE_URL")
api_key = config.get("API_KEY")
```

### Example 4: Validation

```python
from pydantic import BaseModel

class DatabaseConfig(BaseModel):
    url: str
    port: int = 5432

class AppConfig(BaseModel):
    database: DatabaseConfig
    debug: bool = False

# Load and validate
config = ConfigManager.load_from_file("config.json")
validated = config.validate(AppConfig)
```

## 🌟 Real-World Applications

Config loaders are used in:

1. **Web Applications**: Managing database connections, API keys, and feature flags
2. **Microservices**: Service-specific configuration management
3. **Data Pipelines**: ETL job configuration and parameters
4. **Development Tools**: IDE settings, build configurations
5. **Cloud Applications**: Environment-specific configuration management

## 🔧 Troubleshooting

### Common Issues

**1. File Not Found**

```
FileNotFoundError: Configuration file not found: config.json
```

**Solution**: Ensure the file exists and the path is correct.

**2. Invalid File Format**

```
ValueError: Invalid JSON format in config.json: Expecting ',' delimiter
```

**Solution**: Check the file format and syntax.

**3. Validation Error**

```
ValidationError: Configuration validation failed
```

**Solution**: Ensure your configuration matches the Pydantic model schema.

**4. Unsupported File Format**

```
ValueError: Unsupported file format: .txt. Supported: .json, .yaml, .yml, .toml, .env
```

**Solution**: Use a supported file format or add a custom loader.

## 📖 Further Reading

- [Pydantic Documentation](https://docs.pydantic.dev/) - Data validation library
- [Strategy Pattern - Refactoring Guru](https://refactoring.guru/design-patterns/strategy) - Design pattern explanation
- [Python File I/O](https://docs.python.org/3/tutorial/inputoutput.html) - Official Python documentation
- [Configuration Management Best Practices](https://12factor.net/config) - The Twelve-Factor App

## 🎓 Teaching Notes

This lab is ideal for:

- **University Course**: Software engineering, design patterns
- **Workshop**: Configuration management and file I/O
- **Tutorial**: Pydantic validation and type safety
- **Interview Prep**: Design patterns and Python best practices

**Estimated time**: 2-3 hours for complete implementation and testing

**Prerequisites**: Basic Python knowledge, understanding of file I/O, familiarity with dictionaries

---

[← Back to Main README](../../README.md) | [View Examples →](./examples/basic_usage.py)
