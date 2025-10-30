"""Demo script for the function calling agent exercise.

This script demonstrates how to use the function calling agent
to interact with files in the current directory.
"""

import os
import sys

# Add the parent directory to the path so we can import the exercise
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exercises.function_calling_agent import (
    agent_rules,
    list_files,
    read_file,
    terminate,
    tool_functions,
    tools,
)


def demo_individual_tools():
    """Demonstrate the individual tools without the agent loop."""
    print("🔧 Function Calling Agent - Tool Demonstration")
    print("=" * 60)

    print("\n1. Available Tools:")
    for name, func in tool_functions.items():
        print(f"   - {name}: {func.__doc__}")

    print("\n2. Tool Definitions:")
    for tool in tools:
        func_def = tool["function"]
        print(f"   - {func_def['name']}: {func_def['description']}")

    print("\n3. Agent Rules:")
    for rule in agent_rules:
        print(f"   - {rule['role']}: {rule['content'][:100]}...")

    print("\n4. Testing Tools:")

    # Test list_files
    print("\n   📁 Listing files in current directory:")
    files = list_files()
    for file in files[:5]:  # Show first 5 files
        print(f"      - {file}")
    if len(files) > 5:
        print(f"      ... and {len(files) - 5} more files")

    # Test read_file with README
    print("\n   📄 Reading README.md:")
    content = read_file("README.md")
    if content.startswith("Error:"):
        print(f"      {content}")
    else:
        print(f"      File content (first 150 chars): {content[:150]}...")

    # Test terminate
    print("\n   🛑 Testing terminate function:")
    with open(os.devnull, "w") as devnull:
        import sys

        original_stdout = sys.stdout
        sys.stdout = devnull
        terminate("Demo termination message")
        sys.stdout = original_stdout
    print("      Terminate function executed successfully")


def demo_agent_workflow():
    """Demonstrate the agent workflow concept."""
    print("\n🤖 Function Calling Agent - Workflow Demonstration")
    print("=" * 60)

    print("\nThe agent workflow follows these steps:")
    print("1. User provides a task or question")
    print("2. Agent receives the request and available tools")
    print("3. LLM decides which tool(s) to use based on the request")
    print("4. Agent executes the selected tool(s)")
    print("5. Results are added to conversation memory")
    print("6. Process repeats until task is complete or terminated")

    print("\nExample conversation flow:")
    print("User: 'What files are in this directory?'")
    print("Agent: [Calls list_files tool]")
    print("Agent: 'Here are the files: file1.py, file2.txt, ...'")
    print("User: 'Read the contents of file1.py'")
    print("Agent: [Calls read_file tool with 'file1.py']")
    print("Agent: 'Here are the contents of file1.py: ...'")
    print("Agent: [Calls terminate tool]")
    print("Agent: 'Task completed. Summary: ...'")


if __name__ == "__main__":
    print("Function Calling Agent Demo")
    print("Choose a demonstration:")
    print("1. Individual tools")
    print("2. Agent workflow")
    print("3. Both")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == "1":
        demo_individual_tools()
    elif choice == "2":
        demo_agent_workflow()
    elif choice == "3":
        demo_individual_tools()
        demo_agent_workflow()
    else:
        print("Invalid choice. Running both demonstrations.")
        demo_individual_tools()
        demo_agent_workflow()
