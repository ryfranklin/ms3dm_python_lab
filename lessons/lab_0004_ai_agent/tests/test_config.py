"""Tests for the configuration module."""

import os
import tempfile
from unittest.mock import patch

import pytest
from dotenv import load_dotenv

from ..ai_agent.config import Config


class TestConfig:
    """Test cases for the Config class."""

    def test_init_with_default_env_file(self):
        """Test Config initialization with default .env file."""
        # Test that load_dotenv is called when using default constructor
        with patch(
            "lessons.lab_0004_ai_agent.ai_agent.config.load_dotenv"
        ) as mock_load_dotenv:
            Config()
            mock_load_dotenv.assert_called_once_with()

    def test_init_with_custom_env_file(self):
        """Test Config initialization with custom .env file."""
        custom_env_file = "/path/to/custom/.env"
        with patch(
            "lessons.lab_0004_ai_agent.ai_agent.config.load_dotenv"
        ) as mock_load_dotenv:
            Config(env_file=custom_env_file)
            mock_load_dotenv.assert_called_once_with(custom_env_file)

    def test_init_with_none_env_file(self):
        """Test Config initialization with None env_file."""
        with patch(
            "lessons.lab_0004_ai_agent.ai_agent.config.load_dotenv"
        ) as mock_load_dotenv:
            Config(env_file=None)
            mock_load_dotenv.assert_called_once_with()

    def test_openai_api_key_from_env_file(self):
        """Test successful retrieval of OpenAI API key from actual .env file."""
        # Load the actual .env file from project root
        env_file_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            ),
            ".env",
        )

        # Check if .env file exists
        if os.path.exists(env_file_path):
            # Create a new Config instance that loads the actual .env file
            config = Config(env_file=env_file_path)

            # Test that the API key is loaded (should not raise ValueError)
            try:
                api_key = config.openai_api_key
                assert api_key is not None
                assert len(api_key) > 0
                assert api_key.startswith(
                    "sk-"
                )  # OpenAI API keys typically start with "sk-"
            except ValueError as e:
                pytest.fail(
                    f"Failed to load OPENAI_API_KEY from .env file: {e}"
                )
        else:
            pytest.skip("No .env file found in project root")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"})
    def test_openai_api_key_from_environment(self):
        """Test successful retrieval of OpenAI API key from environment variables."""
        config = Config()
        assert config.openai_api_key == "test-api-key"

    def test_openai_api_key_missing(self):
        """Test ValueError when OpenAI API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            # Mock load_dotenv to not load any environment variables
            with patch(
                "lessons.lab_0004_ai_agent.ai_agent.config.load_dotenv"
            ):
                # Create a new Config instance that doesn't load any env vars
                config = Config()
                with pytest.raises(ValueError) as exc_info:
                    _ = config.openai_api_key
                assert (
                    "OPENAI_API_KEY not found in environment variables"
                    in str(exc_info.value)
                )

    @patch.dict(os.environ, {"OPENAI_API_KEY": ""})
    def test_openai_api_key_empty(self):
        """Test ValueError when OpenAI API key is empty."""
        config = Config()
        with pytest.raises(ValueError) as exc_info:
            _ = config.openai_api_key
        assert "OPENAI_API_KEY not found in environment variables" in str(
            exc_info.value
        )

    @patch.dict(os.environ, {"OPENAI_MODEL": "openai/gpt-3.5-turbo"})
    def test_default_model_custom(self):
        """Test custom default model from environment."""
        config = Config()
        assert config.default_model == "openai/gpt-3.5-turbo"

    @patch.dict(os.environ, {}, clear=True)
    def test_default_model_fallback(self):
        """Test fallback to default model when not set."""
        config = Config()
        assert config.default_model == "openai/gpt-4o"

    @patch.dict(os.environ, {"OPENAI_MAX_TOKENS": "2048"})
    def test_default_max_tokens_custom(self):
        """Test custom max tokens from environment."""
        config = Config()
        assert config.default_max_tokens == 2048

    @patch.dict(os.environ, {}, clear=True)
    def test_default_max_tokens_fallback(self):
        """Test fallback to default max tokens when not set."""
        config = Config()
        assert config.default_max_tokens == 1024

    @patch.dict(os.environ, {"OPENAI_MAX_TOKENS": "invalid"})
    def test_default_max_tokens_invalid(self):
        """Test ValueError when max tokens is not a valid integer."""
        config = Config()
        with pytest.raises(ValueError):
            _ = config.default_max_tokens

    @patch.dict(os.environ, {"OPENAI_TEMPERATURE": "0.5"})
    def test_default_temperature_custom(self):
        """Test custom temperature from environment."""
        config = Config()
        assert config.default_temperature == 0.5

    @patch.dict(os.environ, {}, clear=True)
    def test_default_temperature_fallback(self):
        """Test fallback to default temperature when not set."""
        config = Config()
        assert config.default_temperature == 0.7

    @patch.dict(os.environ, {"OPENAI_TEMPERATURE": "invalid"})
    def test_default_temperature_invalid(self):
        """Test ValueError when temperature is not a valid float."""
        config = Config()
        with pytest.raises(ValueError):
            _ = config.default_temperature

    @patch.dict(
        os.environ,
        {
            "OPENAI_API_KEY": "test-key",
            "OPENAI_MODEL": "openai/gpt-3.5-turbo",
            "OPENAI_MAX_TOKENS": "512",
            "OPENAI_TEMPERATURE": "0.3",
        },
    )
    def test_all_properties_with_custom_values(self):
        """Test all properties with custom environment values."""
        config = Config()
        assert config.openai_api_key == "test-key"
        assert config.default_model == "openai/gpt-3.5-turbo"
        assert config.default_max_tokens == 512
        assert config.default_temperature == 0.3

    def test_global_config_instance(self):
        """Test that global config instance is created."""
        from ..ai_agent.config import config

        assert isinstance(config, Config)

    def test_global_config_with_real_env(self):
        """Test that global config instance works with real .env file."""
        # Load the actual .env file from project root
        env_file_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            ),
            ".env",
        )

        if os.path.exists(env_file_path):
            # Load the .env file manually to ensure it's available
            load_dotenv(env_file_path)

            # Import the global config after loading the env
            from ..ai_agent.config import config

            # Test that the global config can access the API key
            try:
                api_key = config.openai_api_key
                assert api_key is not None
                assert len(api_key) > 0
            except ValueError as e:
                pytest.fail(
                    f"Global config failed to load OPENAI_API_KEY: {e}"
                )
        else:
            pytest.skip("No .env file found in project root")


class TestConfigIntegration:
    """Integration tests for Config class with actual .env files."""

    def test_config_with_real_env_file(self):
        """Test Config with the actual .env file from project root."""
        # Load the actual .env file from project root
        env_file_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            ),
            ".env",
        )

        if os.path.exists(env_file_path):
            # Create a new Config instance that loads the actual .env file
            config = Config(env_file=env_file_path)

            # Test that all properties can be accessed without errors
            try:
                api_key = config.openai_api_key
                model = config.default_model
                max_tokens = config.default_max_tokens
                temperature = config.default_temperature

                # Verify the values are reasonable
                assert api_key is not None
                assert len(api_key) > 0
                assert model is not None
                assert isinstance(max_tokens, int)
                assert max_tokens > 0
                assert isinstance(temperature, float)
                assert 0.0 <= temperature <= 2.0

                print("✅ Successfully loaded config from .env:")
                print(f"   Model: {model}")
                print(f"   Max tokens: {max_tokens}")
                print(f"   Temperature: {temperature}")
                print(f"   API key: {api_key[:10]}...")

            except ValueError as e:
                pytest.fail(
                    f"Failed to load configuration from .env file: {e}"
                )
        else:
            pytest.skip("No .env file found in project root")

    def test_config_with_temp_env_file(self):
        """Test Config with a temporary .env file."""
        env_content = """OPENAI_API_KEY=temp-test-key
OPENAI_MODEL=openai/gpt-3.5-turbo
OPENAI_MAX_TOKENS=256
OPENAI_TEMPERATURE=0.8
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write(env_content)
            f.flush()

            try:
                with (
                    patch.dict(os.environ, {}, clear=True),
                    patch(
                        "lessons.lab_0004_ai_agent.ai_agent.config.load_dotenv"
                    ) as mock_load_dotenv,
                ):
                    # Mock load_dotenv to load our test content
                    def mock_load_dotenv_side_effect(env_file=None):
                        if env_file == f.name:
                            # Simulate loading the temp file
                            os.environ.update(
                                {
                                    "OPENAI_API_KEY": "temp-test-key",
                                    "OPENAI_MODEL": "openai/gpt-3.5-turbo",
                                    "OPENAI_MAX_TOKENS": "256",
                                    "OPENAI_TEMPERATURE": "0.8",
                                }
                            )

                    mock_load_dotenv.side_effect = mock_load_dotenv_side_effect
                    config = Config(env_file=f.name)
                    assert config.openai_api_key == "temp-test-key"
                    assert config.default_model == "openai/gpt-3.5-turbo"
                    assert config.default_max_tokens == 256
                    assert config.default_temperature == 0.8
            finally:
                os.unlink(f.name)

    def test_config_with_malformed_env_file(self):
        """Test Config with malformed .env file."""
        env_content = """OPENAI_API_KEY=test-key
OPENAI_MAX_TOKENS=not-a-number
OPENAI_TEMPERATURE=also-not-a-number
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write(env_content)
            f.flush()

            try:
                with (
                    patch.dict(os.environ, {}, clear=True),
                    patch(
                        "lessons.lab_0004_ai_agent.ai_agent.config.load_dotenv"
                    ) as mock_load_dotenv,
                ):
                    # Mock load_dotenv to load our test content
                    def mock_load_dotenv_side_effect(env_file=None):
                        if env_file == f.name:
                            # Simulate loading the temp file
                            os.environ.update(
                                {
                                    "OPENAI_API_KEY": "test-key",
                                    "OPENAI_MAX_TOKENS": "not-a-number",
                                    "OPENAI_TEMPERATURE": "also-not-a-number",
                                }
                            )

                    mock_load_dotenv.side_effect = mock_load_dotenv_side_effect
                    config = Config(env_file=f.name)
                    # API key should work
                    assert config.openai_api_key == "test-key"
                    # But max_tokens and temperature should raise ValueError
                    with pytest.raises(ValueError):
                        _ = config.default_max_tokens
                    with pytest.raises(ValueError):
                        _ = config.default_temperature
            finally:
                os.unlink(f.name)
