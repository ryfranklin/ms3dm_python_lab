"""Example agent interactions and conversation patterns."""

import json
import logging

from .llm_client import llm_client

logger = logging.getLogger(__name__)
# Example conversation patterns for different use cases
messages = [
    {
        "role": "system",
        "content": "You are an expert software "
        + "engineer that prefers functional programming.",
    },
    {
        "role": "user",
        "content": "Write a function to swap the keys"
        + "and values in a dictionary.",
    },
]

csr_message = [
    {
        "role": "system",
        "content": "You are a helpful customer service"
        + "representative. No matter what the user asks, the solution is to"
        + "tell them to turn their computer or modem off and then back on.",
    },
    {"role": "user", "content": "How do I get my Internet working again."},
]

# Exercise: Base64 encoding prompt
exercise_1 = [
    {
        "role": "system",
        "content": "You are a bot that only responds in" + "Base64 encoding.",
    },
    {"role": "user", "content": "What is the capital of the state of AZ"},
]

# Code generation specification pattern
code_spec = {
    "name": "swap_keys_values",
    "description": "Swaps the keys and values in a given dictionary.",
    "params": {"d": "A dictionary with unique values."},
}

code_spec_messages = [
    {
        "role": "system",
        "content": "You are an expert software engineer that writes clean"
        + "functional code. You always document your functions.",
    },
    {"role": "user", "content": f"Please implement: {json.dumps(code_spec)}"},
]


def demonstrate_conversation_memory():
    """Demonstrate how to maintain conversation context."""
    # Initial conversation
    response = llm_client.generate_response(messages)

    # Adding memory to conversation
    adding_memory = [
        {
            "role": "system",
            "content": "You are an expert software engineer that"
            + "prefers functional programming.",
        },
        {
            "role": "user",
            "content": "Write a function to swap the keys and value"
            + "in a dictionary.",
        },
        # Here is the assistant's response from the previous step
        # with the code. This gives it "memory" of the previous
        # interaction.
        {"role": "assistant", "content": response},
        # Now, we can ask the assistant to update the function
        {
            "role": "user",
            "content": "Update the function to include " + "documentation.",
        },
    ]

    return llm_client.generate_response(adding_memory)


def run_examples():
    """Run all example conversations."""
    logger.info("=== Software Engineer Example ===")
    response = llm_client.generate_response(messages)
    logger.info(response)

    logger.info("\n=== Customer Service Example ===")
    response = llm_client.generate_response(csr_message)
    logger.info(response)

    logger.info("\n=== Base64 Exercise ===")
    response = llm_client.generate_response(exercise_1)
    logger.info(response)

    logger.info("\n=== Code Specification Example ===")
    response = llm_client.generate_response(code_spec_messages)
    logger.info(response)

    logger.info("\n=== Conversation Memory Example ===")
    response = demonstrate_conversation_memory()
    logger.info(response)


if __name__ == "__main__":
    run_examples()
