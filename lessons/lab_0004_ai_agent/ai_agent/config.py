"""Configuration module for API settings and environment variables."""

import os

from dotenv import load_dotenv


class Config:
    """Configuration class to manage environment variables and API settings."""

    def __init__(self, env_file: str | None = None):
        """
        Initialize configuration.

        Args:
            env_file: Optional path to .env file. If None, uses default .env
            in project root.
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

    @property
    def openai_api_key(self) -> str:
        """Get OpenAI API key from environment variables."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please check your .env file."
            )
        return api_key

    @property
    def default_model(self) -> str:
        """Get default OpenAI model."""
        return os.getenv("OPENAI_MODEL", "openai/gpt-4o")

    @property
    def default_max_tokens(self) -> int:
        """Get default max tokens for API calls."""
        return int(os.getenv("OPENAI_MAX_TOKENS", "1024"))

    @property
    def default_temperature(self) -> float:
        """Get default temperature for API calls."""
        return float(os.getenv("OPENAI_TEMPERATURE", "0.7"))


# Global configuration instance
config = Config()
