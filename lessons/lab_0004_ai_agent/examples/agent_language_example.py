"""Agent Language Examples - Demonstrating Different Communication Patterns.

This example demonstrates the Agent Language concept, which defines how agents
communicate with Large Language Models through standardized protocols.

The Agent Language abstraction allows agents to use different communication
styles:
- Function Calling: Structured JSON-based action format
- Text-Only: Natural language action descriptions

This separation enables:
- Easy swapping of communication protocols
- Custom communication formats for specific use cases
- Clear separation between agent logic and LLM communication
"""

import sys
from pathlib import Path
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_agent.game_framework import (
    AgentFunctionCallingActionLanguage,
    AgentLanguage,
    AgentTextLanguage,
    Goal,
)


def demonstrate_function_calling_language():
    """Demonstrate function calling agent language."""
    print("=" * 70)
    print("Function Calling Agent Language")
    print("=" * 70)
    print()

    language: AgentLanguage = AgentFunctionCallingActionLanguage()

    # Format an action using JSON
    action_name = "read_file"
    args = {"file_name": "example.txt"}
    formatted = language.format_action(action_name, args)
    print(f"Formatted action: {formatted}")
    print()

    # Parse the action back
    action_name_parsed, args_parsed = language.parse_action(formatted)
    print(f"Parsed - Action: {action_name_parsed}, Args: {args_parsed}")
    print()

    # Format system prompt with goals
    goals = [
        Goal(
            priority=1, name="Read Files", description="Read and process files"
        ),
        Goal(priority=2, name="Analyze", description="Analyze file contents"),
    ]
    system_prompt = language.format_system_prompt(goals)
    print("System Prompt:")
    print(system_prompt)
    print()


def demonstrate_text_language():
    """Demonstrate text-only agent language."""
    print("=" * 70)
    print("Text-Only Agent Language")
    print("=" * 70)
    print()

    language: AgentLanguage = AgentTextLanguage()

    # Format an action using natural language
    action_name = "read file"
    args = {"file_name": "example.txt"}
    formatted = language.format_action(action_name, args)
    print(f"Formatted action: {formatted}")
    print()

    # Parse the action back
    action_name_parsed, args_parsed = language.parse_action(formatted)
    print(f"Parsed - Action: {action_name_parsed}, Args: {args_parsed}")
    print()

    # Format system prompt with goals
    goals = [
        Goal(
            priority=1,
            name="Understand Requests",
            description="Understand user requests in natural language",
        ),
        Goal(
            priority=2, name="Respond", description="Provide helpful responses"
        ),
    ]
    system_prompt = language.format_system_prompt(goals)
    print("System Prompt:")
    print(system_prompt)
    print()


def demonstrate_language_comparison():
    """Compare different agent language formats."""
    print("=" * 70)
    print("Agent Language Comparison")
    print("=" * 70)
    print()

    action_name = "search_database"
    args = {"query": "python", "limit": 10}

    # Function calling format
    func_lang = AgentFunctionCallingActionLanguage()
    func_formatted = func_lang.format_action(action_name, args)
    print("Function Calling Format:")
    print(f"  {func_formatted}")
    print()

    # Text format
    text_lang = AgentTextLanguage()
    text_formatted = text_lang.format_action(action_name, args)
    print("Text Format:")
    print(f"  {text_formatted}")
    print()

    print("Key Differences:")
    print("  - Function Calling: Structured JSON, precise parameter encoding")
    print("  - Text Format: Natural language, more human-readable")
    print(
        "  - Both serve the same purpose but use different communication styles"
    )
    print()


def demonstrate_extensibility():
    """Demonstrate how to create custom agent languages."""

    class CustomAgentLanguage(AgentLanguage):
        """Custom agent language using XML-like format."""

        def format_action(self, action_name: str, args: dict[str, Any]) -> str:
            """Format action in custom XML-like format."""

            args_xml = "".join(
                f'<param name="{k}">{v}</param>' for k, v in args.items()
            )
            return f'<action name="{action_name}">{args_xml}</action>'

        def parse_action(self, content: str) -> tuple[str, dict[str, Any]]:
            """Parse custom XML-like format."""
            # Simplified parser for demonstration
            import re

            name_match = re.search(r'name="([^"]+)"', content)
            if not name_match:
                raise ValueError(f"Invalid action format: {content}")

            action_name = name_match.group(1)
            args = {}
            for param_match in re.finditer(
                r'<param name="([^"]+)">([^<]+)</param>', content
            ):
                args[param_match.group(1)] = param_match.group(2)

            return action_name, args

    print("=" * 70)
    print("Custom Agent Language (XML-like format)")
    print("=" * 70)
    print()

    language = CustomAgentLanguage()
    action_name = "execute_command"
    args = {"command": "ls", "directory": "/home/user"}
    formatted = language.format_action(action_name, args)
    print(f"Custom formatted action: {formatted}")
    print()

    action_name_parsed, args_parsed = language.parse_action(formatted)
    print(f"Parsed - Action: {action_name_parsed}, Args: {args_parsed}")
    print()


def main():
    """Run all agent language demonstrations."""
    print("\n" + "=" * 70)
    print("Agent Language Examples")
    print("=" * 70)
    print()
    print(
        "The Agent Language defines how agents communicate with LLMs through"
    )
    print(
        "standardized protocols for formatting messages and interpreting responses."
    )
    print()

    demonstrate_function_calling_language()
    demonstrate_text_language()
    demonstrate_language_comparison()
    demonstrate_extensibility()

    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print()
    print("Agent Language Benefits:")
    print("  1. Standardized Communication: Consistent message formats")
    print("  2. Extensibility: Easy to create custom communication protocols")
    print(
        "  3. Separation of Concerns: Agent logic separate from LLM interface"
    )
    print("  4. Flexibility: Switch between different languages as needed")
    print()


if __name__ == "__main__":
    main()
