# 📝 Logging Implementation Guide

This guide covers the modern logging implementation in the Python Learning Lab project, including setup, configuration, and best practices.

## 🎯 Overview

The project now uses a centralized, industry-standard logging system that replaces all `print()` statements with appropriate logging calls. This provides better control, formatting, and integration with monitoring systems.

## 🏗️ Architecture

### Core Logging Module

The logging system is centralized in `core/logging_config.py` and provides:

- **Structured logging** with consistent formatting
- **Multiple output destinations** (console, file, structured JSON)
- **Color-coded console output** for better readability
- **Configurable log levels** and filtering
- **Performance logging utilities**
- **Error context logging**

### Key Components

1. **`setup_logging()`** - Main configuration function
2. **`get_logger()`** - Get logger instances
3. **`quick_setup()`** - Fast setup for simple cases
4. **Utility functions** - Performance, error, and function call logging

## 🚀 Quick Start

### Basic Setup

```python
from core import setup_logging, get_logger

# Set up logging
setup_logging(level="INFO")
logger = get_logger(__name__)

# Use the logger
logger.info("Application started")
logger.error("Something went wrong")
```

### Advanced Setup

```python
from core import setup_logging, get_logger

# Advanced configuration
setup_logging(
    level="DEBUG",
    log_file="app.log",
    enable_console=True,
    enable_colors=True,
    structured=False
)

logger = get_logger(__name__)
```

## ⚙️ Configuration Options

### Log Levels

- **DEBUG**: Detailed information for diagnosing problems
- **INFO**: General information about program execution
- **WARNING**: Something unexpected happened, but the program is still working
- **ERROR**: A serious problem occurred
- **CRITICAL**: A very serious error occurred

### Output Destinations

#### Console Output

```python
setup_logging(
    enable_console=True,
    enable_colors=True  # Colored output for terminals
)
```

#### File Output

```python
setup_logging(
    log_file="application.log",
    enable_console=False
)
```

#### Structured JSON Logging

```python
setup_logging(
    structured=True,
    log_file="structured.log"
)
```

### Formatters

The system includes several built-in formatters:

1. **Standard**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
2. **Colored**: Same as standard but with ANSI colors
3. **Detailed**: Includes filename, line number, and function name
4. **Structured**: JSON format for log aggregation systems

## 📋 Usage Examples

### Basic Logging

```python
import logging
from core import setup_logging, get_logger

setup_logging(level="INFO")
logger = get_logger(__name__)

def process_data(data):
    logger.info(f"Processing {len(data)} records")

    try:
        result = perform_operation(data)
        logger.info("Data processing completed successfully")
        return result
    except Exception as e:
        logger.error(f"Data processing failed: {e}")
        raise
```

### Performance Logging

```python
from core import log_performance
import time

def expensive_operation():
    start_time = time.time()

    # Perform work
    time.sleep(2)

    # Log performance
    log_performance(logger, "expensive_operation", time.time() - start_time)
```

### Function Call Logging

```python
from core import log_function_call

def calculate_total(items, tax_rate):
    log_function_call(logger, "calculate_total", items=len(items), tax_rate=tax_rate)

    # Function implementation
    pass
```

### Error Context Logging

```python
from core import log_error_with_context

def risky_operation():
    try:
        # Risky operation
        pass
    except Exception as e:
        log_error_with_context(logger, e, "risky_operation")
        raise
```

## 🔧 Configuration Files

### External Configuration

You can use external logging configuration files:

```python
# logging.conf
[loggers]
keys=root

[handlers]
keys=console,file

[formatters]
keys=standard

[logger_root]
level=INFO
handlers=console,file

[handler_console]
class=StreamHandler
level=INFO
formatter=standard
args=(sys.stdout,)

[handler_file]
class=FileHandler
level=DEBUG
formatter=standard
args=('app.log',)

[formatter_standard]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

```python
# Use external config
setup_logging(config_file="logging.conf")
```

## 🎨 Console Output

### Colored Output

The system automatically detects terminal capabilities and applies colors:

- **DEBUG**: Dim white
- **INFO**: Green
- **WARNING**: Yellow
- **ERROR**: Red
- **CRITICAL**: Bold red

### Example Output

```
2024-01-15 10:30:45 - myapp.module - INFO - Application started
2024-01-15 10:30:46 - myapp.module - DEBUG - Processing user data
2024-01-15 10:30:47 - myapp.module - WARNING - Rate limit approaching
2024-01-15 10:30:48 - myapp.module - ERROR - Database connection failed
```

## 📊 Structured Logging

For production environments and log aggregation:

```python
setup_logging(
    structured=True,
    log_file="app.json.log"
)
```

Produces JSON output:

```json
{
  "timestamp": "2024-01-15 10:30:45",
  "logger": "myapp.module",
  "level": "INFO",
  "file": "module.py",
  "line": 42,
  "function": "process_data",
  "message": "Data processing completed"
}
```

## 🏷️ Logger Hierarchy

The system uses Python's logger hierarchy:

```
python_learning_lab
├── lessons
│   ├── lab_0001_event_bus
│   ├── lab_0002_config_loader
│   ├── lab_0004_ai_agent
│   └── lab_0005_snowflake
├── core
└── examples
```

Each module gets its own logger namespace for fine-grained control.

## 🔍 Third-Party Library Logging

The system reduces noise from third-party libraries:

```python
'loggers': {
    'urllib3': {'level': 'WARNING'},
    'requests': {'level': 'WARNING'},
    'snowflake': {'level': 'INFO'},
    'snowflake.connector': {'level': 'WARNING'},
}
```

## 📁 Log File Management

### Rotating Files

Log files automatically rotate when they reach 10MB:

```python
setup_logging(
    log_file="app.log",
    # Automatically configured:
    # maxBytes=10485760,  # 10MB
    # backupCount=5
)
```

### File Locations

- **Development**: Logs in project root
- **Production**: Configure via environment variables
- **Docker**: Mount volume for persistent logs

## 🧪 Testing with Logging

### Capturing Logs in Tests

```python
import logging
from io import StringIO
from core import setup_logging, get_logger

def test_logging():
    # Capture log output
    log_capture = StringIO()
    handler = logging.StreamHandler(log_capture)

    setup_logging(level="INFO")
    logger = get_logger("test")
    logger.addHandler(handler)

    logger.info("Test message")

    assert "Test message" in log_capture.getvalue()
```

### Disabling Logs in Tests

```python
import logging

# Disable all logging during tests
logging.disable(logging.CRITICAL)
```

## 🚀 Production Considerations

### Environment Variables

```bash
# Set log level
export LOG_LEVEL=INFO

# Set log file
export LOG_FILE=/var/log/app.log

# Enable structured logging
export STRUCTURED_LOGGING=true
```

### Docker Integration

```dockerfile
# Create log directory
RUN mkdir -p /var/log/app

# Set environment
ENV LOG_FILE=/var/log/app/application.log
ENV LOG_LEVEL=INFO
```

### Monitoring Integration

The structured JSON format works with:

- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Fluentd**
- **Splunk**
- **Datadog**
- **New Relic**

## 📚 Best Practices

### 1. Use Appropriate Log Levels

```python
# Good
logger.debug("Processing item %d", item_id)
logger.info("User %s logged in", username)
logger.warning("Rate limit approaching: %d requests", count)
logger.error("Database connection failed: %s", error)

# Avoid
logger.info("DEBUG: Processing item")  # Wrong level
logger.error("User logged in")  # Wrong level
```

### 2. Include Context

```python
# Good
logger.info("Processing order %s for user %s", order_id, user_id)

# Avoid
logger.info("Processing order")
```

### 3. Use Structured Data

```python
# Good
logger.info("User action", extra={
    "user_id": user_id,
    "action": "login",
    "ip_address": request.remote_addr
})

# Avoid
logger.info(f"User {user_id} performed {action} from {ip}")
```

### 4. Don't Log Sensitive Information

```python
# Good
logger.info("User authentication successful", extra={"user_id": user_id})

# Avoid
logger.info(f"User {username} password {password} is correct")
```

### 5. Use Exception Logging

```python
# Good
try:
    risky_operation()
except Exception as e:
    logger.exception("Operation failed")  # Includes traceback
    raise

# Or with context
try:
    risky_operation()
except Exception as e:
    log_error_with_context(logger, e, "risky_operation")
    raise
```

## 🔄 Migration from print()

### Before (print statements)

```python
def process_data(data):
    print("Processing data...")
    try:
        result = perform_operation(data)
        print("Success!")
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise
```

### After (logging)

```python
from core import setup_logging, get_logger

setup_logging(level="INFO")
logger = get_logger(__name__)

def process_data(data):
    logger.info("Processing data...")
    try:
        result = perform_operation(data)
        logger.info("Success!")
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

## 🛠️ Troubleshooting

### Common Issues

1. **No log output**: Check log level configuration
2. **Missing colors**: Ensure terminal supports ANSI colors
3. **File permissions**: Check write permissions for log files
4. **Performance**: Use appropriate log levels in production

### Debug Mode

```python
# Enable debug logging
setup_logging(level="DEBUG")
logger = get_logger(__name__)

# Log configuration
logger.debug("Logging configured with level: %s", logging.getLevelName(logger.level))
```

## 📖 Further Reading

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Logging Best Practices](https://docs.python.org/3/howto/logging.html)
- [Structured Logging](https://www.structlog.org/)
- [ELK Stack Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

## 🤝 Contributing

When adding new features or modifying existing code:

1. Replace `print()` statements with appropriate logging calls
2. Use the centralized logging configuration
3. Follow the established patterns and conventions
4. Test logging output in different environments
5. Update this guide if adding new logging features

---

*This logging system provides a solid foundation for monitoring, debugging, and maintaining the Python Learning Lab project in both development and production environments.*
