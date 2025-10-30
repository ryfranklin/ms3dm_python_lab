"""GAME Framework Exercise - Building a Modular Agent.

This exercise demonstrates how to build a file explorer agent using the GAME
framework (Goals, Actions, Memory, Environment). The GAME framework provides
a structured approach to building AI agents by separating concerns into:

- Goals: Define what the agent should accomplish
- Actions: Define the tools/functions available to the agent
- Memory: Track conversation history and agent state
- Environment: Represent the agent's execution context

This is an evolution from the direct function-calling approach to a more
modular, extensible architecture.

Reference: Building a Simple Agent Framework from Coursera AI Agents course
"""

import os
from typing import Any

from ai_agent.game_framework import (
    Action,
    ActionRegistry,
    Agent,
    AgentFunctionCallingActionLanguage,
    Environment,
    Goal,
    Memory,
)
from litellm import completion


def list_files() -> list[str]:
    """List files in the current directory."""
    return os.listdir(".")


def read_file(file_name: str) -> str:
    """Read a file's contents."""
    try:
        with open(file_name) as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found."
    except Exception as e:
        return f"Error: {str(e)}"


def terminate(message: str) -> str:
    """Terminate the agent loop and provide a summary message."""
    return message


def generate_response(messages: list[dict], tools: list[dict]) -> Any:
    """Generate response from LLM with tool support."""
    return completion(
        model="openai/gpt-4o",
        messages=messages,
        tools=tools,
        max_tokens=1024,
        stream=False,
    )


def main():
    """Main function demonstrating the GAME framework."""
    print("🎮 GAME Framework Exercise - File Explorer Agent")
    print("=" * 60)
    print("This exercise demonstrates the GAME framework:")
    print("  - Goals: What the agent should accomplish")
    print("  - Actions: Tools available to the agent")
    print("  - Memory: Conversation history")
    print("  - Environment: Execution context")
    print()

    # Define clear goals for the agent
    goals = [
        Goal(
            priority=1,
            name="Explore Files",
            description="Explore files in the current directory by listing and reading them",
        ),
        Goal(
            priority=2,
            name="Terminate",
            description="Terminate the session when tasks are complete with a helpful summary",
        ),
    ]

    print("📋 Agent Goals:")
    for goal in goals:
        print(f"  • {goal.name}: {goal.description}")

    # Create action registry and register actions
    action_registry = ActionRegistry()

    action_registry.register(
        Action(
            name="list_files",
            function=list_files,
            description="Returns a list of files in the directory.",
            parameters={},
            terminal=False,
        )
    )

    action_registry.register(
        Action(
            name="read_file",
            function=read_file,
            description="Reads the content of a specified file in the directory.",
            parameters={
                "type": "object",
                "properties": {"file_name": {"type": "string"}},
                "required": ["file_name"],
            },
            terminal=False,
        )
    )

    action_registry.register(
        Action(
            name="terminate",
            function=terminate,
            description="Terminates the conversation. Prints the provided message for the user.",
            parameters={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                },
                "required": ["message"],
            },
            terminal=True,
        )
    )

    print("\n🔧 Available Actions:")
    for name, action in action_registry.get_all().items():
        print(f"  • {name}: {action.description}")

    # Define the agent language and environment
    agent_language = AgentFunctionCallingActionLanguage()
    environment = Environment(working_directory=".")

    # Create the agent
    file_explorer_agent = Agent(
        goals=goals,
        agent_language=agent_language,
        action_registry=action_registry,
        generate_response=generate_response,
        environment=environment,
    )

    print("\n✅ Agent created successfully!")
    print("\n" + "=" * 60)
    print("Starting agent...")
    print()

    # Get user input
    user_input = input("What would you like me to do? ")

    # Run the agent
    final_memory = file_explorer_agent.run(user_input, max_iterations=10)

    # Print the final conversation
    print("\n" + "=" * 60)
    print("📝 Final Conversation History:")
    print("=" * 60)
    for item in final_memory.get_memories():
        if isinstance(item, dict):
            if item.get("role") == "user":
                print(f"\n👤 USER: {item.get('content', '')}")
            elif item.get("role") == "assistant":
                print(f"\n🤖 ASSISTANT: {item.get('content', '')}")


def demonstrate_goals_and_actions():
    """Demonstrate the concepts of Goals and Actions separately."""
    print("\n🎓 Framework Concepts Demonstration")
    print("=" * 60)

    # Demonstrate Goals
    print("\n1. Goals - Define what the agent should accomplish:")
    example_goals = [
        Goal(priority=1, name="Get Information", description="Retrieve data"),
        Goal(
            priority=2, name="Process Data", description="Analyze information"
        ),
        Goal(priority=3, name="Respond", description="Provide answer to user"),
    ]

    print("   Goals (sorted by priority):")
    for goal in sorted(example_goals):
        print(f"     {goal}")

    # Demonstrate Actions
    print("\n2. Actions - Tools the agent can use:")
    registry = ActionRegistry()
    registry.register(
        Action(
            name="example_action",
            function=lambda x: x,
            description="An example action",
            parameters={"type": "object", "properties": {}, "required": []},
        )
    )

    print("   Registered actions:")
    for name, action in registry.get_all().items():
        print(f"     • {name}: {action.description}")

    print("\n3. Memory - Tracks conversation state:")
    memory = Memory()
    memory.add("user_input", "Hello, agent!")
    memory.add("assistant_response", "Hello, human!")
    print(f"   Memory entries: {len(memory)}")
    print(f"   Memories: {memory.get_memories()}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demonstrate_goals_and_actions()
    else:
        main()
