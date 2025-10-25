"""
Centralized logging configuration for the Python Learning Lab.

This module provides a standardized logging setup that can be used across
all labs and examples. It includes structured logging, proper formatting,
and configurable output destinations.
"""

import logging
import logging.config
import sys
from pathlib import Path
from typing import Any


# Color codes for console output
class Colors:
    """ANSI color codes for console output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels."""

    COLORS = {
        "DEBUG": Colors.DIM + Colors.WHITE,
        "INFO": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
        "CRITICAL": Colors.BOLD + Colors.RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with colors."""
        # Get the base formatted message
        formatted = super().format(record)

        # Add color if we're outputting to a terminal
        if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
            color = self.COLORS.get(record.levelname, "")
            if color:
                formatted = f"{color}{formatted}{Colors.RESET}"

        return formatted


def get_logging_config(
    level: str = "INFO",
    log_file: str | None = None,
    enable_console: bool = True,
    enable_colors: bool = True,
    structured: bool = False,
) -> dict[str, Any]:
    """
    Get logging configuration dictionary.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        enable_console: Whether to enable console output
        enable_colors: Whether to enable colored console output
        structured: Whether to use structured JSON logging

    Returns:
        Logging configuration dictionary
    """
    handlers = {}
    root_handlers = []

    # Console handler
    if enable_console:
        handlers["console"] = {
            "class": "logging.StreamHandler",
            "level": level,
            "formatter": "colored" if enable_colors else "standard",
            "stream": "ext://sys.stdout",
        }
        root_handlers.append("console")

    # File handler
    if log_file:
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": level,
            "formatter": "structured" if structured else "detailed",
            "filename": log_file,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        }
        root_handlers.append("file")

    # Formatters
    formatters = {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "colored": {
            "()": "core.logging_config.ColoredFormatter",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "structured": {
            "format": '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "file": "%(filename)s", "line": %(lineno)d, "function": "%(funcName)s", "message": "%(message)s"}',
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": formatters,
        "handlers": handlers,
        "root": {"level": level, "handlers": root_handlers},
        "loggers": {
            # Reduce noise from third-party libraries
            "urllib3": {"level": "WARNING"},
            "requests": {"level": "WARNING"},
            "snowflake": {"level": "INFO"},
            "snowflake.connector": {"level": "WARNING"},
            # Our application loggers
            "python_learning_lab": {
                "level": level,
                "propagate": False,
                "handlers": root_handlers,
            },
            "lessons": {
                "level": level,
                "propagate": False,
                "handlers": root_handlers,
            },
            "core": {
                "level": level,
                "propagate": False,
                "handlers": root_handlers,
            },
        },
    }

    return config


def setup_logging(
    level: str = "INFO",
    log_file: str | None = None,
    enable_console: bool = True,
    enable_colors: bool = True,
    structured: bool = False,
    config_file: str | None = None,
) -> None:
    """
    Set up logging configuration for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        enable_console: Whether to enable console output
        enable_colors: Whether to enable colored console output
        structured: Whether to use structured JSON logging
        config_file: Optional path to external logging config file
    """
    if config_file and Path(config_file).exists():
        # Load from external config file
        logging.config.fileConfig(config_file)
    else:
        # Use our default configuration
        config = get_logging_config(
            level=level,
            log_file=log_file,
            enable_console=enable_console,
            enable_colors=enable_colors,
            structured=structured,
        )
        logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def log_function_call(
    logger: logging.Logger, func_name: str, **kwargs
) -> None:
    """
    Log a function call with its parameters.

    Args:
        logger: Logger instance
        func_name: Name of the function being called
        **kwargs: Function parameters to log
    """
    params = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.debug(f"Calling {func_name}({params})")


def log_performance(
    logger: logging.Logger, operation: str, duration: float
) -> None:
    """
    Log performance metrics.

    Args:
        logger: Logger instance
        operation: Name of the operation
        duration: Duration in seconds
    """
    logger.info(f"Performance: {operation} completed in {duration:.3f}s")


def log_error_with_context(
    logger: logging.Logger, error: Exception, context: str = ""
) -> None:
    """
    Log an error with additional context.

    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Additional context about where the error occurred
    """
    context_msg = f" in {context}" if context else ""
    logger.error(f"Error{context_msg}: {type(error).__name__}: {error}")


# Convenience function for quick setup
def quick_setup(level: str = "INFO") -> logging.Logger:
    """
    Quick setup for basic logging.

    Args:
        level: Logging level

    Returns:
        Logger instance
    """
    setup_logging(level=level)
    return get_logger(__name__)


# Example usage and testing
if __name__ == "__main__":
    # Example of different logging setups

    print("=== Basic Setup ===")
    logger = quick_setup("DEBUG")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    print("\n=== With File Logging ===")
    setup_logging(level="INFO", log_file="test.log")
    logger = get_logger("test")
    logger.info("This will be written to both console and file")

    print("\n=== Structured Logging ===")
    setup_logging(level="INFO", structured=True, log_file="structured.log")
    logger = get_logger("structured")
    logger.info("This is structured JSON logging")

    print("\n=== Performance Logging ===")
    import time

    logger = get_logger("performance")
    start = time.time()
    time.sleep(0.1)  # Simulate work
    log_performance(logger, "test_operation", time.time() - start)
