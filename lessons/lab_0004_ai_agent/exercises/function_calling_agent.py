"""Function calling agent exercise - demonstrates tool usage with AI agents.

This exercise shows how to create an AI agent that can use tools (functions)
to interact with the file system. The agent can list files, read file contents,
and terminate the conversation based on user requests.
"""

import json
import os

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


def terminate(message: str) -> None:
    """Terminate the agent loop and provide a summary message."""
    print(f"Termination message: {message}")


# Tool function registry
tool_functions = {
    "list_files": list_files,
    "read_file": read_file,
    "terminate": terminate,
}

# Tool definitions for the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Returns a list of files in the directory.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file in the directory.",
            "parameters": {
                "type": "object",
                "properties": {"file_name": {"type": "string"}},
                "required": ["file_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "terminate",
            "description": "Terminates the conversation. No further actions or interactions are possible after this. Prints the provided message for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                },
                "required": ["message"],
            },
        },
    },
]

# Agent system rules
agent_rules = [
    {
        "role": "system",
        "content": """
You are an AI agent that can perform tasks by using available tools.

If a user asks about files, documents, or content, first list the files before reading them.

When you are done, terminate the conversation by using the "terminate" tool and I will provide the results to the user.
""",
    }
]


def run_function_calling_agent():
    """Run the function calling agent exercise."""
    print("🤖 Function Calling Agent Exercise")
    print("=" * 50)
    print("This agent can help you explore files in the current directory.")
    print(
        "Try asking it to list files, read specific files, or analyze content."
    )
    print()

    # Initialize agent parameters
    iterations = 0
    max_iterations = 10

    user_task = input("What would you like me to do? ")

    memory = [{"role": "user", "content": user_task}]

    # The Agent Loop
    while iterations < max_iterations:
        print(f"\n--- Iteration {iterations + 1} ---")

        messages = agent_rules + memory

        try:
            response = completion(
                model="openai/gpt-4o",
                messages=messages,
                tools=tools,
                max_tokens=1024,
                stream=False,
            )

            if response.choices[0].message.tool_calls:  # type: ignore
                tool = response.choices[0].message.tool_calls[0]  # type: ignore
                tool_name = tool.function.name
                tool_args = json.loads(tool.function.arguments)

                action = {"tool_name": tool_name, "args": tool_args}

                if tool_name == "terminate":
                    print(f"Termination message: {tool_args['message']}")
                    break
                elif tool_name in tool_functions:
                    try:
                        result = {
                            "result": tool_functions[tool_name](**tool_args)
                        }
                    except Exception as e:
                        result = {
                            "error": f"Error executing {tool_name}: {str(e)}"
                        }
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}

                print(f"Executing: {tool_name} with args {tool_args}")
                print(f"Result: {result}")
                memory.extend(
                    [
                        {"role": "assistant", "content": json.dumps(action)},
                        {"role": "user", "content": json.dumps(result)},
                    ]
                )
            else:
                result = response.choices[0].message.content  # type: ignore
                print(f"Response: {result}")
                break

        except Exception as e:
            print(f"Error in agent loop: {e}")
            break

        iterations += 1

    if iterations >= max_iterations:
        print(
            f"\n⚠️  Maximum iterations ({max_iterations}) reached. Agent stopped."
        )


def demonstrate_tool_usage():
    """Demonstrate the individual tools without the agent loop."""
    print("🔧 Tool Demonstration")
    print("=" * 30)

    print("\n1. Listing files in current directory:")
    files = list_files()
    for file in files[:10]:  # Show first 10 files
        print(f"  - {file}")
    if len(files) > 10:
        print(f"  ... and {len(files) - 10} more files")

    print("\n2. Reading a sample file (README.md):")
    content = read_file("README.md")
    if content.startswith("Error:"):
        print(f"  {content}")
    else:
        print(f"  File content (first 200 chars): {content[:200]}...")

    print("\n3. Tool functions available:")
    for name, func in tool_functions.items():
        print(f"  - {name}: {func.__doc__}")


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Run the function calling agent")
    print("2. Demonstrate individual tools")
    print("3. Both")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == "1":
        run_function_calling_agent()
    elif choice == "2":
        demonstrate_tool_usage()
    elif choice == "3":
        demonstrate_tool_usage()
        print("\n" + "=" * 60)
        run_function_calling_agent()
    else:
        print("Invalid choice. Running function calling agent by default.")
        run_function_calling_agent()
