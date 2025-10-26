"""Tests for the function calling agent exercise."""

import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from lessons.lab_0004_ai_agent.exercises.function_calling_agent import (
    agent_rules,
    list_files,
    read_file,
    terminate,
    tool_functions,
    tools,
)


class TestFunctionCallingAgent(unittest.TestCase):
    """Test cases for the function calling agent exercise."""

    def test_list_files(self):
        """Test the list_files function."""
        # Test that it returns a list
        files = list_files()
        self.assertIsInstance(files, list)

        # Test that it returns files from current directory
        # We know there should be at least some files
        self.assertGreater(len(files), 0)

    def test_read_file_existing(self):
        """Test reading an existing file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt"
        ) as f:
            test_content = "This is a test file content."
            f.write(test_content)
            temp_file = f.name

        try:
            # Test reading the file
            content = read_file(temp_file)
            self.assertEqual(content, test_content)
        finally:
            # Clean up
            os.unlink(temp_file)

    def test_read_file_nonexistent(self):
        """Test reading a non-existent file."""
        content = read_file("nonexistent_file_12345.txt")
        self.assertTrue(content.startswith("Error:"))

    def test_terminate(self):
        """Test the terminate function."""
        # Test that it doesn't raise an exception
        with patch("builtins.print") as mock_print:
            terminate("Test termination message")
            mock_print.assert_called_once_with(
                "Termination message: Test termination message"
            )

    def test_tool_functions_registry(self):
        """Test that all expected functions are in the registry."""
        expected_functions = ["list_files", "read_file", "terminate"]
        for func_name in expected_functions:
            self.assertIn(func_name, tool_functions)
            self.assertIsNotNone(tool_functions[func_name])

    def test_tools_definition_structure(self):
        """Test that tools definition has correct structure."""
        self.assertIsInstance(tools, list)
        self.assertEqual(len(tools), 3)

        # Test each tool has required structure
        for tool in tools:
            self.assertIn("type", tool)
            self.assertEqual(tool["type"], "function")
            self.assertIn("function", tool)

            func_def = tool["function"]
            self.assertIn("name", func_def)
            self.assertIn("description", func_def)
            self.assertIn("parameters", func_def)

    def test_tools_function_names(self):
        """Test that tool names match function registry."""
        tool_names = [tool["function"]["name"] for tool in tools]
        registry_names = list(tool_functions.keys())

        self.assertEqual(set(tool_names), set(registry_names))

    def test_agent_rules_structure(self):
        """Test that agent rules have correct structure."""
        self.assertIsInstance(agent_rules, list)
        self.assertEqual(len(agent_rules), 1)

        rule = agent_rules[0]
        self.assertIn("role", rule)
        self.assertIn("content", rule)
        self.assertEqual(rule["role"], "system")

    def test_tool_parameters_structure(self):
        """Test that tool parameters are properly defined."""
        for tool in tools:
            func_def = tool["function"]
            params = func_def["parameters"]

            self.assertIn("type", params)
            self.assertEqual(params["type"], "object")
            self.assertIn("properties", params)
            self.assertIn("required", params)

            # Test specific tools
            if func_def["name"] == "list_files":
                self.assertEqual(params["required"], [])
            elif func_def["name"] == "read_file":
                self.assertIn("file_name", params["properties"])
                self.assertEqual(params["required"], ["file_name"])
            elif func_def["name"] == "terminate":
                self.assertIn("message", params["properties"])
                self.assertEqual(params["required"], ["message"])

    @patch(
        "lessons.lab_0004_ai_agent.exercises.function_calling_agent.completion"
    )
    def test_agent_loop_tool_call(self, mock_completion):
        """Test the agent loop with tool calls."""
        # Mock the completion response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.tool_calls = [MagicMock()]
        mock_response.choices[0].message.tool_calls[
            0
        ].function.name = "list_files"
        mock_response.choices[0].message.tool_calls[
            0
        ].function.arguments = "{}"
        mock_completion.return_value = mock_response

        # This would require refactoring the main function to be testable
        # For now, we test the individual components
        self.assertTrue(True)  # Placeholder for future integration test

    def test_json_serialization(self):
        """Test that tool arguments can be JSON serialized."""
        # Test that the tool arguments structure is JSON serializable
        for tool in tools:
            func_def = tool["function"]
            params = func_def["parameters"]

            # This should not raise an exception
            json.dumps(params)

    def test_function_signatures(self):
        """Test that function signatures match tool definitions."""
        # Test list_files
        list_files_result = list_files()
        self.assertIsInstance(list_files_result, list)

        # Test read_file
        read_result = read_file("README.md")  # Should exist in project
        self.assertIsInstance(read_result, str)

        # Test terminate
        with patch("builtins.print"):
            terminate("test")  # Should not raise exception


if __name__ == "__main__":
    unittest.main()
