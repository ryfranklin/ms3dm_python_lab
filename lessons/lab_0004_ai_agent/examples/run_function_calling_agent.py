"""Example script to run the function calling agent.

This script provides a simple way to run the function calling agent
with some example prompts to get you started.
"""

import os
import sys

# Add the parent directory to the path so we can import the exercise
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exercises.function_calling_agent import run_function_calling_agent


def main():
    """Run the function calling agent with example prompts."""
    print("🤖 Function Calling Agent - Example Runner")
    print("=" * 50)
    print()
    print("This agent can help you explore files in the current directory.")
    print("Here are some example prompts you can try:")
    print()
    print("1. 'List all the files in this directory'")
    print("2. 'What files are here and read the README'")
    print("3. 'Show me the contents of the main Python files'")
    print("4. 'Find all .py files and read their first few lines'")
    print("5. 'Analyze the project structure and summarize what you find'")
    print()
    print("Or ask your own question!")
    print()

    # Run the function calling agent
    run_function_calling_agent()


if __name__ == "__main__":
    main()
