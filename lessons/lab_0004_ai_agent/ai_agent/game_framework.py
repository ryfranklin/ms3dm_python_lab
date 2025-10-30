"""GAME Framework - Goal, Action, Memory, Environment for AI Agents.

This module implements the GAME framework for building modular, goal-driven AI agents.
The framework separates concerns into Goals, Actions, Memory management, and
Environment interaction, making it easy to build and maintain AI agents.

The Agent Language concept defines how agents communicate with LLMs through
standardized protocols for formatting messages, handling responses, and managing
interactions.

Classes:
    Goal: Represents an agent's objective with priority and description
    Action: Represents a tool or function the agent can execute
    ActionRegistry: Manages a collection of available actions
    Memory: Stores conversation history and agent state
    Environment: Represents the agent's execution environment
    AgentLanguage: Abstract base class for agent-LLM communication protocols
    AgentFunctionCallingActionLanguage: Handles LLM function calling interactions
    AgentTextLanguage: Handles text-only LLM interactions
    Agent: Orchestrates goal-driven agent execution
"""

import json
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Goal:
    """Represents an agent's goal with priority and description."""

    priority: int
    name: str
    description: str

    def __lt__(self, other: "Goal") -> bool:
        """Compare goals by priority (lower number = higher priority)."""
        return self.priority < other.priority

    def __str__(self) -> str:
        return f"Goal(priority={self.priority}, name={self.name}, description={self.description})"


@dataclass
class Action:
    """Represents an action/tool that an agent can execute."""

    name: str
    function: Callable
    description: str
    parameters: dict[str, Any]
    terminal: bool = False


class ActionRegistry:
    """Registry for managing available actions."""

    def __init__(self):
        """Initialize an empty action registry."""
        self._actions: dict[str, Action] = {}

    def register(self, action: Action) -> None:
        """Register an action in the registry."""
        self._actions[action.name] = action

    def get(self, name: str) -> Action | None:
        """Get an action by name."""
        return self._actions.get(name)

    def get_all(self) -> dict[str, Action]:
        """Get all registered actions."""
        return self._actions.copy()

    def get_tool_specs(self) -> list[dict[str, Any]]:
        """Convert registered actions to tool specifications for LLM."""
        tools = []
        for action in self._actions.values():
            tool = {
                "type": "function",
                "function": {
                    "name": action.name,
                    "description": action.description,
                    "parameters": action.parameters,
                },
            }
            tools.append(tool)
        return tools


class Memory:
    """Stores conversation history and agent state."""

    def __init__(self, initial_memory: list[dict[str, Any]] | None = None):
        """Initialize memory with optional initial state."""
        self._memories: list[dict[str, Any]] = initial_memory or []

    def add(
        self, type: str, content: str, metadata: dict[str, Any] | None = None
    ) -> None:
        """Add a memory entry."""
        memory_entry: dict[str, Any] = {"type": type, "content": content}
        if metadata:
            memory_entry["metadata"] = metadata
        self._memories.append(memory_entry)

    def extend(self, memories: list[dict[str, Any]]) -> None:
        """Add multiple memory entries."""
        self._memories.extend(memories)

    def get_memories(self) -> list[dict[str, Any]]:
        """Get all memories."""
        return self._memories.copy()

    def clear(self) -> None:
        """Clear all memories."""
        self._memories = []

    def __len__(self) -> int:
        return len(self._memories)


class Environment:
    """Represents the agent's execution environment."""

    def __init__(self, **kwargs):
        """Initialize environment with optional configuration."""
        self.config = kwargs

    def update(self, **kwargs) -> None:
        """Update environment configuration."""
        self.config.update(kwargs)

    def get(self, key: str, default: Any = None) -> Any:
        """Get environment configuration value."""
        return self.config.get(key, default)


class AgentLanguage(ABC):
    """Abstract base class for agent-LLM communication protocols.

    The Agent Language defines how an agent formats messages, interprets responses,
    and manages the communication protocol with Large Language Models. Different
    implementations can support various interaction patterns like function calling,
    text-only conversations, or structured responses.

    Subclasses must implement methods for formatting messages, parsing responses,
    and handling different types of agent-LLM interactions.
    """

    def __init__(self) -> None:
        """Initialize the agent language handler."""
        pass

    @abstractmethod
    def format_action(self, action_name: str, args: dict[str, Any]) -> str:
        """Format an action for LLM interaction.

        Args:
            action_name: Name of the action to execute
            args: Arguments for the action

        Returns:
            Formatted string representation of the action
        """
        pass

    @abstractmethod
    def parse_action(self, content: str) -> tuple[str, dict[str, Any]]:
        """Parse an action from LLM response.

        Args:
            content: Response content from LLM

        Returns:
            Tuple of (action_name, args) parsed from content

        Raises:
            ValueError: If content cannot be parsed
        """
        pass

    def format_system_prompt(self, goals: list["Goal"]) -> str:
        """Format system prompt with agent goals.

        Args:
            goals: List of agent goals

        Returns:
            Formatted system prompt string
        """
        goals_description = "\n".join(
            [
                f"  {i+1}. {goal.name} (Priority: {goal.priority}): {goal.description}"
                for i, goal in enumerate(sorted(goals))
            ]
        )
        return f"""You are an AI agent that can perform tasks.

Your goals are:
{goals_description}

Execute actions to accomplish these goals."""

    def format_response_for_memory(
        self, action_name: str, args: dict[str, Any]
    ) -> dict[str, Any]:
        """Format an action response for memory storage.

        Args:
            action_name: Name of the action executed
            args: Arguments used for the action

        Returns:
            Dictionary formatted for memory storage
        """
        return {
            "role": "assistant",
            "content": self.format_action(action_name, args),
        }

    def extract_tool_calls(
        self, llm_response: Any
    ) -> list[dict[str, Any]] | None:
        """Extract tool calls from LLM response.

        Args:
            llm_response: Response object from LLM

        Returns:
            List of tool call dictionaries or None if no tool calls
        """
        # Default implementation - subclasses override for specific formats
        if hasattr(llm_response, "choices") and llm_response.choices:
            message = llm_response.choices[0].message
            if hasattr(message, "tool_calls") and message.tool_calls:
                return [
                    {
                        "name": tool.function.name,
                        "arguments": json.loads(tool.function.arguments),
                    }
                    for tool in message.tool_calls
                ]
        return None


class AgentFunctionCallingActionLanguage(AgentLanguage):
    """Handles LLM function calling interactions.

    This implementation supports the function calling protocol where the LLM
    can invoke tools/functions defined in the action registry. The language
    format uses JSON to encode action names and arguments.

    Example:
        >>> language = AgentFunctionCallingActionLanguage()
        >>> formatted = language.format_action("read_file", {"file_name": "test.txt"})
        >>> assert '{"tool_name": "read_file"' in formatted
    """

    def format_action(self, action_name: str, args: dict[str, Any]) -> str:
        """Format an action using JSON encoding.

        The format follows: {"tool_name": "<name>", "args": {...}}

        Args:
            action_name: Name of the action to execute
            args: Arguments for the action

        Returns:
            JSON-encoded action string
        """
        return json.dumps({"tool_name": action_name, "args": args})

    def parse_action(self, content: str) -> tuple[str, dict[str, Any]]:
        """Parse a JSON-encoded action.

        Args:
            content: JSON string containing action information

        Returns:
            Tuple of (action_name, args) parsed from JSON

        Raises:
            ValueError: If content is not valid JSON or missing required fields
        """
        try:
            data = json.loads(content)
            return data["tool_name"], data["args"]
        except (json.JSONDecodeError, KeyError) as err:
            raise ValueError(f"Invalid action format: {content}") from err


class AgentTextLanguage(AgentLanguage):
    """Handles text-only LLM interactions without function calling.

    This implementation is for agents that communicate purely through text
    messages. Actions may be described in natural language within the conversation,
    and the agent must interpret and respond to requests conversationally.

    Example:
        >>> language = AgentTextLanguage()
        >>> # Actions are described in natural language
        >>> formatted = language.format_action("read file", {"file_name": "test.txt"})
        >>> assert "read file" in formatted.lower()
    """

    def format_action(self, action_name: str, args: dict[str, Any]) -> str:
        """Format an action as natural language text.

        Args:
            action_name: Name of the action to execute
            args: Arguments for the action

        Returns:
            Natural language description of the action
        """
        if args:
            args_str = ", ".join(f"{k}={v}" for k, v in args.items())
            return f"Action: {action_name} with parameters: {args_str}"
        return f"Action: {action_name}"

    def parse_action(self, content: str) -> tuple[str, dict[str, Any]]:
        """Parse action from natural language text.

        This is a basic implementation that looks for "Action:" prefix.
        More sophisticated implementations could use NLP to extract actions.

        Args:
            content: Text containing action description

        Returns:
            Tuple of (action_name, args) parsed from text

        Raises:
            ValueError: If content cannot be parsed as an action
        """
        if not content.strip().startswith("Action:"):
            raise ValueError(f"Text does not contain an action: {content}")

        # Simple parsing - remove "Action:" prefix
        action_text = content.replace("Action:", "").strip()

        # Try to extract action name and args
        if " with parameters: " in action_text:
            action_name, params_str = action_text.split(
                " with parameters: ", 1
            )
            # Simple parameter parsing - more sophisticated parsing could be added
            args = {}
            for param in params_str.split(","):
                if "=" in param:
                    key, value = param.split("=", 1)
                    args[key.strip()] = value.strip()
            return action_name.strip(), args

        # Return action name and empty args
        action_name = action_text.split()[0] if action_text else ""
        return (action_name, {})


@dataclass
class Agent:
    """Orchestrates goal-driven agent execution."""

    goals: list[Goal]
    agent_language: AgentLanguage
    action_registry: ActionRegistry
    generate_response: Callable[
        [list[dict[str, Any]], list[dict[str, Any]]], Any
    ]
    environment: Environment
    max_iterations: int = 10

    def __post_init__(self):
        """Sort goals by priority after initialization."""
        self.goals = sorted(self.goals)

    def run(
        self, user_input: str, max_iterations: int | None = None
    ) -> Memory:
        """
        Run the agent with user input.

        Args:
            user_input: The user's request or question
            max_iterations: Maximum number of iterations (overrides default)

        Returns:
            Memory object containing conversation history
        """
        max_iter = max_iterations or self.max_iterations
        memory = Memory(
            initial_memory=[{"role": "user", "content": user_input}]
        )

        # Build system prompt using agent language
        base_prompt = self.agent_language.format_system_prompt(self.goals)
        system_prompt = f"""{base_prompt}

If a user asks about files, documents, or content, first list the files before reading them.

When you are done, terminate the conversation by using the "terminate" tool if available."""

        system_rules = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        iterations = 0
        terminal = False

        while iterations < max_iter and not terminal:
            print(f"\n--- Iteration {iterations + 1} ---")

            messages = system_rules + memory.get_memories()
            tools = self.action_registry.get_tool_specs()

            try:
                response = self.generate_response(messages, tools)

                if response.choices[0].message.tool_calls:  # type: ignore
                    tool = response.choices[0].message.tool_calls[0]  # type: ignore
                    tool_name = tool.function.name
                    tool_args = json.loads(tool.function.arguments)

                    # Use agent language to format the action
                    formatted_action = self.agent_language.format_action(
                        tool_name, tool_args
                    )
                    print(f"Agent Decision: {tool_name} with args {tool_args}")

                    # Execute the action
                    agent_action = self.action_registry.get(tool_name)
                    if agent_action is None:
                        result = {"error": f"Unknown action: {tool_name}"}
                    else:
                        try:
                            action_result = agent_action.function(**tool_args)
                            result = {
                                "tool_executed": True,
                                "result": action_result,
                            }
                        except Exception as e:
                            result = {
                                "error": f"Error executing {tool_name}: {str(e)}"
                            }

                    # Check if this is a terminal action
                    if agent_action and agent_action.terminal:
                        terminal = True
                        print(
                            f"Termination: {tool_args.get('message', 'Completed')}"
                        )

                    # Update memory using agent language formatting
                    memory.extend(
                        [
                            {
                                "role": "assistant",
                                "content": formatted_action,
                            },
                            {"role": "user", "content": json.dumps(result)},
                        ]
                    )
                else:
                    # No tool call, just text response
                    content = response.choices[0].message.content  # type: ignore
                    print(f"Response: {content}")
                    memory.add("response", content)
                    terminal = True

            except Exception as e:
                print(f"Error in agent loop: {e}")
                memory.add("error", str(e))
                break

            iterations += 1

        if iterations >= max_iter and not terminal:
            print(
                f"\n⚠️  Maximum iterations ({max_iter}) reached. Agent stopped."
            )
            memory.add("warning", f"Maximum iterations ({max_iter}) reached")

        return memory
