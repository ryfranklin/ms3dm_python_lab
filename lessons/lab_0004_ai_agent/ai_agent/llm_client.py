"""LLM client module for abstracting language model interactions."""

from typing import Any

from litellm import completion

from .config import config


class LLMClient:
    """Client for interacting with language models through LiteLLM."""

    def __init__(
        self,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ):
        """
        Initialize LLM client.

        Args:
            model: Model to use. If None, uses default from config.
            max_tokens: Maximum tokens for response. If None, uses
            default from config.
            temperature: Temperature for response generation. If None, uses
            default from config.
        """
        self.model = model or config.default_model
        self.max_tokens = max_tokens or config.default_max_tokens
        self.temperature = temperature or config.default_temperature

    def generate_response(self, messages: list[dict[str, str]]) -> str:
        """
        Generate a response from the language model.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            keys.

        Returns:
            Generated response as a string.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response: Any = completion(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            content = response.choices[0].message.content
            if content is None:
                raise Exception("Received empty response from LLM")
            return content
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}") from e

    def chat(self, system_prompt: str, user_message: str) -> str:
        """
        Convenience method for simple chat interactions.

        Args:
            system_prompt: System message to set the context.
            user_message: User's message.

        Returns:
            Generated response as a string.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        return self.generate_response(messages)

    def update_settings(
        self,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ):
        """
        Update client settings.

        Args:
            model: New model to use.
            max_tokens: New max tokens setting.
            temperature: New temperature setting.
        """
        if model is not None:
            self.model = model
        if max_tokens is not None:
            self.max_tokens = max_tokens
        if temperature is not None:
            self.temperature = temperature


# Global client instance
llm_client = LLMClient()
