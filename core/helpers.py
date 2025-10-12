"""
Shared helper functions and utilities for all labs.
"""


def format_lesson_number(num: int) -> str:
    """
    Format a lesson number as a zero-padded string.

    Args:
        num: The lesson number

    Returns:
        A zero-padded 4-digit string (e.g., '0001')

    Examples:
        >>> format_lesson_number(1)
        '0001'
        >>> format_lesson_number(42)
        '0042'
    """
    assert isinstance(num, int), "Lesson number must be an integer"
    assert num > 0, "Lesson number must be positive"

    return f"{num:04d}"


def validate_not_none(value, name: str):
    """
    Assert that a value is not None.

    Args:
        value: The value to check
        name: The name of the value (for error messages)

    Raises:
        AssertionError: If value is None
    """
    assert value is not None, f"{name} cannot be None"
