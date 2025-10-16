"""Tests for the LLM client module."""

from unittest.mock import MagicMock, patch

import pytest

from ..ai_agent.llm_client import LLMClient


class TestLLMClient:
    """Test cases for the LLMClient class."""

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_init_with_defaults(self, mock_config):
        """Test LLMClient initialization with default values."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        client = LLMClient()

        assert client.model == "openai/gpt-4o"
        assert client.max_tokens == 1024
        assert client.temperature == 0.7

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_init_with_custom_values(self, mock_config):
        """Test LLMClient initialization with custom values."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        client = LLMClient(
            model="openai/gpt-3.5-turbo", max_tokens=512, temperature=0.5
        )

        assert client.model == "openai/gpt-3.5-turbo"
        assert client.max_tokens == 512
        assert client.temperature == 0.5

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_init_with_partial_custom_values(self, mock_config):
        """Test LLMClient initialization with some custom values."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        client = LLMClient(model="openai/gpt-3.5-turbo")

        assert client.model == "openai/gpt-3.5-turbo"
        assert client.max_tokens == 1024  # Uses default
        assert client.temperature == 0.7  # Uses default

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.completion")
    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_generate_response_success(self, mock_config, mock_completion):
        """Test successful response generation."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        # Mock the completion response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_completion.return_value = mock_response

        client = LLMClient()
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ]

        result = client.generate_response(messages)

        assert result == "Test response"
        mock_completion.assert_called_once_with(
            model="openai/gpt-4o",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.completion")
    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_generate_response_with_custom_settings(
        self, mock_config, mock_completion
    ):
        """Test response generation with custom client settings."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Custom response"
        mock_completion.return_value = mock_response

        client = LLMClient(
            model="openai/gpt-3.5-turbo", max_tokens=512, temperature=0.5
        )

        messages = [{"role": "user", "content": "Test"}]
        result = client.generate_response(messages)

        assert result == "Custom response"
        mock_completion.assert_called_once_with(
            model="openai/gpt-3.5-turbo",
            messages=messages,
            max_tokens=512,
            temperature=0.5,
        )

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.completion")
    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_generate_response_api_error(self, mock_config, mock_completion):
        """Test handling of API errors during response generation."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        mock_completion.side_effect = Exception("API Error")

        client = LLMClient()
        messages = [{"role": "user", "content": "Test"}]

        with pytest.raises(Exception) as exc_info:
            client.generate_response(messages)

        assert "Failed to generate response: API Error" in str(exc_info.value)

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.completion")
    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_chat_method(self, mock_config, mock_completion):
        """Test the chat convenience method."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Chat response"
        mock_completion.return_value = mock_response

        client = LLMClient()
        result = client.chat("You are helpful.", "Hello!")

        assert result == "Chat response"

        expected_messages = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "Hello!"},
        ]
        mock_completion.assert_called_once_with(
            model="openai/gpt-4o",
            messages=expected_messages,
            max_tokens=1024,
            temperature=0.7,
        )

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_update_settings_all_params(self, mock_config):
        """Test updating all client settings."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        client = LLMClient()

        client.update_settings(
            model="openai/gpt-3.5-turbo", max_tokens=512, temperature=0.5
        )

        assert client.model == "openai/gpt-3.5-turbo"
        assert client.max_tokens == 512
        assert client.temperature == 0.5

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_update_settings_partial_params(self, mock_config):
        """Test updating some client settings."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        client = LLMClient()

        client.update_settings(model="openai/gpt-3.5-turbo")

        assert client.model == "openai/gpt-3.5-turbo"
        assert client.max_tokens == 1024  # Unchanged
        assert client.temperature == 0.7  # Unchanged

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_update_settings_none_params(self, mock_config):
        """Test update_settings with None parameters (should not change)."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        client = LLMClient()
        original_model = client.model
        original_max_tokens = client.max_tokens
        original_temperature = client.temperature

        client.update_settings(model=None, max_tokens=None, temperature=None)

        assert client.model == original_model
        assert client.max_tokens == original_max_tokens
        assert client.temperature == original_temperature

    def test_global_llm_client_instance(self):
        """Test that global llm_client instance is created."""
        from ..ai_agent.llm_client import llm_client

        assert isinstance(llm_client, LLMClient)


class TestLLMClientIntegration:
    """Integration tests for LLMClient with mocked API calls."""

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.completion")
    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_full_conversation_flow(self, mock_config, mock_completion):
        """Test a complete conversation flow."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        # Mock responses for a conversation
        responses = [
            "Hello! How can I help you today?",
            "I can help you with that. Here's what you need to do...",
        ]

        mock_completion.side_effect = [
            MagicMock(choices=[MagicMock(message=MagicMock(content=response))])
            for response in responses
        ]

        client = LLMClient()

        # First message
        messages1 = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ]
        response1 = client.generate_response(messages1)

        # Second message with context
        messages2 = messages1 + [
            {"role": "assistant", "content": response1},
            {"role": "user", "content": "Can you help me with Python?"},
        ]
        response2 = client.generate_response(messages2)

        assert response1 == "Hello! How can I help you today?"
        assert (
            response2 == "I can help you with that. Here's what you need "
            "to do..."
        )
        assert mock_completion.call_count == 2

    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.completion")
    @patch("lessons.lab_0004_ai_agent.ai_agent.llm_client.config")
    def test_error_handling_and_recovery(self, mock_config, mock_completion):
        """Test error handling and recovery."""
        mock_config.default_model = "openai/gpt-4o"
        mock_config.default_max_tokens = 1024
        mock_config.default_temperature = 0.7

        client = LLMClient()
        messages = [{"role": "user", "content": "Test"}]

        # First call fails
        mock_completion.side_effect = Exception("Network error")

        with pytest.raises(Exception) as exc_info:
            client.generate_response(messages)
        assert "Failed to generate response: " "Network error" in str(
            exc_info.value
        )

        # Second call succeeds
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Success after retry"
        mock_completion.side_effect = None
        mock_completion.return_value = mock_response

        result = client.generate_response(messages)
        assert result == "Success after retry"
