"""Tests for the agent examples module."""

import json

from ..ai_agent.agent_examples import (
    code_spec,
    code_spec_messages,
    csr_message,
    exercise_1,
    messages,
)


class TestAgentMessages:
    """Test cases for the message structures in agent_examples.py."""

    def test_messages_structure(self):
        """Test the structure of the main messages list."""
        assert isinstance(messages, list)
        assert len(messages) == 2

        # Check system message
        assert messages[0]["role"] == "system"
        assert "expert software engineer" in messages[0]["content"]
        assert "functional programming" in messages[0]["content"]

        # Check user message
        assert messages[1]["role"] == "user"
        assert "swap the keys" in messages[1]["content"]
        assert "dictionary" in messages[1]["content"]

    def test_csr_message_structure(self):
        """Test the structure of the CSR message list."""
        assert isinstance(csr_message, list)
        assert len(csr_message) == 2

        # Check system message
        assert csr_message[0]["role"] == "system"
        assert "customer service" in csr_message[0]["content"]
        assert "turn their computer" in csr_message[0]["content"]

        # Check user message
        assert csr_message[1]["role"] == "user"
        assert "Internet working" in csr_message[1]["content"]

    def test_exercise_1_structure(self):
        """Test the structure of exercise_1 message list."""
        assert isinstance(exercise_1, list)
        assert len(exercise_1) == 2

        # Check system message
        assert exercise_1[0]["role"] == "system"
        assert "Base64 encoding" in exercise_1[0]["content"]

        # Check user message
        assert exercise_1[1]["role"] == "user"
        assert "capital of the state of AZ" in exercise_1[1]["content"]

    def test_code_spec_structure(self):
        """Test the structure of the code specification."""
        assert isinstance(code_spec, dict)
        assert "name" in code_spec
        assert "description" in code_spec
        assert "params" in code_spec

        assert code_spec["name"] == "swap_keys_values"
        assert "Swaps the keys and values" in code_spec["description"]
        assert isinstance(code_spec["params"], dict)
        assert "d" in code_spec["params"]

    def test_code_spec_messages_structure(self):
        """Test the structure of code_spec_messages."""
        assert isinstance(code_spec_messages, list)
        assert len(code_spec_messages) == 2

        # Check system message
        assert code_spec_messages[0]["role"] == "system"
        assert "expert software engineer" in code_spec_messages[0]["content"]
        assert "functional code" in code_spec_messages[0]["content"]

        # Check user message
        assert code_spec_messages[1]["role"] == "user"
        assert "Please implement" in code_spec_messages[1]["content"]

        # Verify JSON is properly embedded
        user_content = code_spec_messages[1]["content"]
        assert json.dumps(code_spec) in user_content


class TestAgentIntegration:
    """Integration tests for the agent examples module."""

    def test_agent_message_structures_are_consistent(self):
        """Test that agent message structures consistent and well-formed."""
        # Test that all message lists have proper structure
        all_message_lists = [
            messages,
            csr_message,
            exercise_1,
            code_spec_messages,
        ]

        for message_list in all_message_lists:
            assert isinstance(message_list, list)
            assert len(message_list) >= 1

            for message in message_list:
                assert isinstance(message, dict)
                assert "role" in message
                assert "content" in message
                assert message["role"] in ["system", "user", "assistant"]
                assert isinstance(message["content"], str)
                assert len(message["content"].strip()) > 0

    def test_json_serialization_in_code_spec(self):
        """Test that code_spec can be properly serialized to JSON."""
        # This should not raise an exception
        json_str = json.dumps(code_spec)
        assert isinstance(json_str, str)

        # Should be able to deserialize back
        deserialized = json.loads(json_str)
        assert deserialized == code_spec

    def test_message_roles_are_valid(self):
        """Test that all message roles are valid."""
        valid_roles = {"system", "user", "assistant"}

        all_messages = [messages, csr_message, exercise_1, code_spec_messages]

        for message_list in all_messages:
            for message in message_list:
                assert message["role"] in valid_roles
                assert "content" in message
                assert isinstance(message["content"], str)
                assert len(message["content"]) > 0

    def test_no_empty_messages(self):
        """Test that no messages have empty content."""
        all_messages = [messages, csr_message, exercise_1, code_spec_messages]

        for message_list in all_messages:
            for message in message_list:
                assert message["content"].strip() != ""

    def test_message_content_quality(self):
        """Test that message content is meaningful and well-formed."""
        # Test that system messages provide clear instructions
        system_messages = []
        all_messages = [messages, csr_message, exercise_1, code_spec_messages]

        for message_list in all_messages:
            for message in message_list:
                if message["role"] == "system":
                    system_messages.append(message["content"])

        # All system messages should be substantial
        for content in system_messages:
            assert len(content) > 20  # Should be more than just a few words
            assert not content.isspace()  # Should not be just whitespace

    def test_code_spec_completeness(self):
        """Test that code_spec contains all necessary fields."""
        required_fields = ["name", "description", "params"]

        for field in required_fields:
            assert field in code_spec
            assert code_spec[field] is not None

        # Test that params is a dictionary with string values
        assert isinstance(code_spec["params"], dict)
        for param_name, param_desc in code_spec["params"].items():
            assert isinstance(param_name, str)
            assert isinstance(param_desc, str)
            assert len(param_name) > 0
            assert len(param_desc) > 0
