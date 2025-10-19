"""
Core utilities shared across all Python Learning Lab lessons.
"""

from .logging_config import (
    get_logger,
    log_error_with_context,
    log_function_call,
    log_performance,
    quick_setup,
    setup_logging,
)

__version__ = "0.1.0"
__all__ = [
    "get_logger",
    "log_error_with_context",
    "log_function_call",
    "log_performance",
    "quick_setup",
    "setup_logging",
]
