# Lab 0004: AI Agent Framework

**Status**: ✅ Complete
**Difficulty**: Intermediate to Advanced
**Concepts**: LLM Integration, Configuration Management, Agent Development, API Abstraction

## 🎯 Learning Objectives

By the end of this lab, you will understand:

- ✅ How to integrate Large Language Models (LLMs) into Python applications
- ✅ Configuration management for API keys and settings
- ✅ Building abstracted clients for LLM interactions
- ✅ Conversation patterns and memory management
- ✅ Interactive agent development workflows
- ✅ Error handling and robust API integration

## 🤖 What is an AI Agent?

An **AI Agent** is a software system that can perceive its environment, make decisions, and take actions to achieve specific goals. In this lab, we focus on conversational agents that:

- **Process natural language** input from users
- **Maintain conversation context** and memory
- **Generate responses** using Large Language Models
- **Execute specific tasks** like code generation and documentation

This pattern is used in many modern applications:

- ChatGPT and similar conversational AI
- Code generation tools (GitHub Copilot, Cursor)
- Customer service chatbots
- Personal AI assistants
- Automated content creation systems

## 🏗️ Architecture

This lab provides a modular AI agent framework:

### 1. **Configuration Management** (`config.py`)

- Environment variable handling
- API key management
- Default settings configuration
- Secure credential storage

### 2. **LLM Client** (`llm_client.py`)

- Abstracted interface to language models
- Support for multiple providers via LiteLLM
- Conversation management
- Error handling and retry logic

### 3. **Agent Examples** (`agent_examples.py`)

- Pre-built conversation patterns
- Different agent personalities
- Code generation workflows
- Memory management demonstrations

### 4. **GAME Framework** (`game_framework.py`)

- Goal-driven agent architecture
- Action registry and tool management
- Memory and conversation tracking
- Environment configuration
- Modular, extensible agent design

### 5. **Agent Language** (`game_framework.py`)

- **Agent Language Protocol**: Defines how agents communicate with LLMs
- **Standardized Communication**: Consistent message formatting and response parsing
- **Multiple Implementations**: Function calling, text-only, and extensible formats
- **Separation of Concerns**: Agent logic separate from LLM interface
- **Flexibility**: Easy to swap communication protocols

The Agent Language is a crucial concept that standardizes the communication protocol between agents and Large Language Models. It defines:

- **Message Formatting**: How actions are encoded for the LLM
- **Response Parsing**: How LLM responses are interpreted
- **Protocol Extensibility**: Easy to create custom communication styles

See [Agent Language Examples](#agent-language-communication-protocols) for detailed usage.

### 6. **Interactive Exercises** (`exercises/`)

- Hands-on function development
- Step-by-step agent interaction
- Real-world coding scenarios
- GAME framework implementation

## 🚀 Quick Start

### Prerequisites

1. **API Key Setup**: You'll need an OpenAI API key
2. **Environment Configuration**: Create a `.env` file in the project root

### Installation

```bash
# From the repository root
cd lessons/lab_0004_ai_agent
```

### Environment Setup

Create a `.env` file in the project root:

```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=openai/gpt-4o
OPENAI_MAX_TOKENS=1024
OPENAI_TEMPERATURE=0.7
```

### Basic Usage

```python
from ai_agent import llm_client

# Simple chat interaction
response = llm_client.chat(
    system_prompt="You are a helpful Python tutor.",
    user_message="Explain list comprehensions with examples."
)
print(response)
```

### Advanced Usage - Conversation Memory

```python
from ai_agent import llm_client

# Start a conversation
messages = [
    {"role": "system", "content": "You are a software engineer."},
    {"role": "user", "content": "Write a function to calculate fibonacci numbers."}
]

# Get initial response
response = llm_client.generate_response(messages)
print("Initial response:", response)

# Add response to conversation history
messages.append({"role": "assistant", "content": response})
messages.append({"role": "user", "content": "Now add error handling to that function."})

# Get updated response with context
updated_response = llm_client.generate_response(messages)
print("Updated response:", updated_response)
```

## 🔍 Key Features

### 1. **Flexible Configuration**

```python
from ai_agent.config import Config

# Custom configuration
config = Config(env_file="custom.env")

# Access settings
api_key = config.openai_api_key
model = config.default_model
max_tokens = config.default_max_tokens
temperature = config.default_temperature
```

### 2. **Multiple LLM Providers**

```python
from ai_agent import LLMClient

# Use different models
gpt4_client = LLMClient(model="openai/gpt-4o")
gpt35_client = LLMClient(model="openai/gpt-3.5-turbo")
claude_client = LLMClient(model="anthropic/claude-3-sonnet")
```

### 3. **Dynamic Settings**

```python
# Update client settings on the fly
llm_client.update_settings(
    model="openai/gpt-4o",
    max_tokens=2048,
    temperature=0.3
)
```

### 4. **Error Handling**

```python
try:
    response = llm_client.generate_response(messages)
except Exception as e:
    print(f"API Error: {e}")
    # Handle gracefully
```

## 🛠️ Interactive Exercises

### Exercise 1: Function Developer

Run the interactive function development tool:

```bash
python exercises/function_developer.py
```

This exercise demonstrates:

- **Multi-step conversation** with memory
- **Code generation** and iteration
- **Documentation** creation
- **Test case** generation
- **File output** management

### Exercise 2: Function Calling Agent

Run the function calling agent exercise:

```bash
python exercises/function_calling_agent.py
```

This exercise demonstrates:

- **Tool integration** with LLM agents
- **Function calling** patterns using LiteLLM
- **File system interaction** through AI agents
- **Agent loop** management and iteration control
- **Tool registry** and parameter validation

#### Function Calling Agent Details

The function calling agent demonstrates how to create an AI agent that can use tools to interact with the environment. Key concepts include:

**Tool Definition**: Each tool is defined with a JSON schema that describes its parameters and requirements:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file in the directory.",
            "parameters": {
                "type": "object",
                "properties": {"file_name": {"type": "string"}},
                "required": ["file_name"]
            }
        }
    }
]
```

**Agent Loop**: The agent processes user requests by calling the LLM with available tools:

```python
response = completion(
    model="openai/gpt-4o",
    messages=messages,
    tools=tools,
    max_tokens=1024
)
```

**Tool Execution**: When the LLM decides to use a tool, the agent executes it and adds the result to the conversation memory:

```python
if response.choices[0].message.tool_calls:
    tool = response.choices[0].message.tool_calls[0]
    tool_name = tool.function.name
    tool_args = json.loads(tool.function.arguments)

    result = tool_functions[tool_name](**tool_args)
    memory.extend([
        {"role": "assistant", "content": json.dumps(action)},
        {"role": "user", "content": json.dumps(result)}
    ])
```

### Exercise 3: GAME Framework Agent

Run the GAME framework exercise to see how to build a modular agent architecture:

```bash
python exercises/game_framework_exercise.py
```

This exercise demonstrates the **GAME framework** (Goals, Actions, Memory, Environment) for building AI agents:

#### Framework Components

**1. Goals** - Define what the agent should accomplish with priorities:

```python
goals = [
    Goal(
        priority=1,
        name="Explore Files",
        description="Explore files in the current directory by listing and reading them"
    ),
    Goal(
        priority=2,
        name="Terminate",
        description="Terminate the session when tasks are complete"
    )
]
```

**2. Actions** - Define tools/functions available to the agent:

```python
action_registry = ActionRegistry()
action_registry.register(Action(
    name="list_files",
    function=list_files,
    description="Returns a list of files in the directory.",
    parameters={},
    terminal=False
))
```

**3. Agent** - Orchestrates goals, actions, and memory:

```python
file_explorer_agent = Agent(
    goals=goals,
    agent_language=agent_language,
    action_registry=action_registry,
    generate_response=generate_response,
    environment=environment
)
```

**4. Running the Agent**:

```python
final_memory = file_explorer_agent.run(user_input, max_iterations=10)
```

#### Benefits of the GAME Framework

- **Better Organization**: Each component has a clear purpose
- **Reusability**: Swap components without changing core logic
- **Extensibility**: Add new goals and actions easily
- **Standard Interface**: Consistent way to interact with agents
- **Memory Management**: Automatic conversation tracking

This structured approach makes it easier to develop, maintain, and extend AI agents as complexity grows.

## 🗣️ Agent Language: Communication Protocols

The **Agent Language** defines the protocol for how agents communicate with Large Language Models. This abstraction enables standardized, extensible communication patterns.

### Understanding Agent Language

Agent Language is the interface between your agent's logic and the LLM's communication protocol. It handles:

1. **Action Formatting**: Encoding agent actions for the LLM
2. **Response Parsing**: Extracting information from LLM responses
3. **System Prompt Formatting**: Structuring agent goals for the LLM
4. **Memory Management**: Formatting responses for conversation history

### Available Agent Languages

#### 1. Function Calling Language (`AgentFunctionCallingActionLanguage`)

Uses structured JSON to encode actions - ideal for function-calling LLMs:

```python
from ai_agent import AgentFunctionCallingActionLanguage

language = AgentFunctionCallingActionLanguage()

# Format action as JSON
action = language.format_action("read_file", {"file_name": "test.txt"})
# Result: '{"tool_name": "read_file", "args": {"file_name": "test.txt"}}'

# Parse action from LLM response
action_name, args = language.parse_action(action)
# Result: ("read_file", {"file_name": "test.txt"})
```

**Best for**: Agents using OpenAI's function calling, structured tool execution

#### 2. Text-Only Language (`AgentTextLanguage`)

Uses natural language descriptions - suitable for text-only interactions:

```python
from ai_agent import AgentTextLanguage

language = AgentTextLanguage()

# Format action as natural language
action = language.format_action("read file", {"file_name": "test.txt"})
# Result: "Action: read file with parameters: file_name=test.txt"

# Parse action from text response
action_name, args = language.parse_action(action)
# Result: ("read file", {"file_name": "test.txt"})
```

**Best for**: Conversational agents, simple text-based interactions

### Creating Custom Agent Languages

Extend the `AgentLanguage` base class to create custom communication protocols:

```python
from ai_agent import AgentLanguage
from typing import Any

class CustomAgentLanguage(AgentLanguage):
    """Custom XML-like format."""

    def format_action(self, action_name: str, args: dict[str, Any]) -> str:
        """Format action in custom format."""
        args_str = " ".join(f'{k}="{v}"' for k, v in args.items())
        return f'<action name="{action_name}" {args_str} />'

    def parse_action(self, content: str) -> tuple[str, dict[str, Any]]:
        """Parse custom format."""
        # Implementation for parsing your format
        import re
        name_match = re.search(r'name="([^"]+)"', content)
        # ... parsing logic
        return action_name, args
```

### Using Agent Language in Agents

```python
from ai_agent import Agent, Goal, AgentFunctionCallingActionLanguage

# Choose your agent language
agent_language = AgentFunctionCallingActionLanguage()

# Create agent with specific language
agent = Agent(
    goals=[Goal(priority=1, name="Task", description="Complete task")],
    agent_language=agent_language,  # Specify communication protocol
    action_registry=action_registry,
    generate_response=generate_response,
    environment=environment
)
```

### Benefits of Agent Language

- **Protocol Standardization**: Consistent communication patterns
- **Easy Protocol Switching**: Change language without modifying agent logic
- **Extensibility**: Create domain-specific communication formats
- **Separation of Concerns**: Agent logic independent of LLM interface

### Example Usage

See `examples/agent_language_example.py` for comprehensive examples demonstrating:

- Function calling language
- Text-only language
- Custom language implementation
- Language comparison and selection

```bash
python examples/agent_language_example.py
```

### Exercise 4: Custom Agent Personality

Create your own agent personality:

```python
from ai_agent import llm_client

# Define custom system prompt
system_prompt = """You are a creative writing assistant.
You help users develop compelling stories, characters, and narratives.
Always provide constructive feedback and creative suggestions."""

# Use in conversation
response = llm_client.chat(
    system_prompt=system_prompt,
    user_message="Help me create a character for a sci-fi novel."
)
```

### Exercise 5: Code Review Agent

```python
# Code review agent
code_reviewer = [
    {"role": "system", "content": "You are an expert code reviewer. "
     "Analyze code for bugs, performance issues, and best practices. "
     "Provide specific, actionable feedback."},
    {"role": "user", "content": "Review this Python function:\n\n"
     "def process_data(items):\n"
     "    result = []\n"
     "    for item in items:\n"
     "        if item > 0:\n"
     "            result.append(item * 2)\n"
     "    return result"}
]

response = llm_client.generate_response(code_reviewer)
```

## 🧪 Running Tests

This lab includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/test_config.py
pytest tests/test_llm_client.py
pytest tests/test_agent_examples.py
pytest tests/test_function_calling_agent.py

# Run with coverage
pytest --cov=ai_agent --cov-report=term-missing

# Run with verbose output
pytest -v
```

Test coverage includes:

- ✅ Configuration management and environment variables
- ✅ LLM client initialization and settings
- ✅ API response handling and error cases
- ✅ Conversation memory and context management
- ✅ Message structure validation
- ✅ Integration scenarios
- ✅ Function calling and tool integration
- ✅ Agent loop management and iteration control

## 💡 Advanced Patterns

### 1. **Agent Memory Management**

```python
class ConversationManager:
    def __init__(self, system_prompt):
        self.messages = [{"role": "system", "content": system_prompt}]

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_response(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def get_response(self, llm_client):
        response = llm_client.generate_response(self.messages)
        self.add_assistant_response(response)
        return response
```

### 2. **Multi-Agent Coordination**

```python
# Specialized agents
code_agent = LLMClient()
code_agent.update_settings(temperature=0.1)  # More deterministic

creative_agent = LLMClient()
creative_agent.update_settings(temperature=0.9)  # More creative

# Use appropriate agent for task
if task_type == "coding":
    response = code_agent.chat("You are a coding expert.", user_input)
else:
    response = creative_agent.chat("You are a creative writer.", user_input)
```

### 3. **Streaming Responses**

```python
from litellm import acompletion
import asyncio

async def stream_response(messages):
    response = await acompletion(
        model="openai/gpt-4o",
        messages=messages,
        stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
```

## 🌟 Real-World Applications

AI agents are used in:

1. **Development Tools**: Code completion, debugging assistance, documentation generation
2. **Customer Support**: Automated responses, ticket routing, FAQ handling
3. **Content Creation**: Blog posts, marketing copy, social media content
4. **Education**: Personalized tutoring, homework help, concept explanation
5. **Business Intelligence**: Data analysis, report generation, insights extraction
6. **Creative Industries**: Story development, character creation, world-building

## 🔧 Troubleshooting

### Common Issues

**1. API Key Not Found**

```
ValueError: OPENAI_API_KEY not found in environment variables
```

**Solution**: Ensure your `.env` file is in the project root and contains a valid API key.

**2. Rate Limiting**

```
Exception: Failed to generate response: Rate limit exceeded
```

**Solution**: Implement exponential backoff or reduce request frequency.

**3. Invalid Model**

```
Exception: Failed to generate response: Model not found
```

**Solution**: Check the model name format (e.g., `openai/gpt-4o`) and ensure you have access.

**4. Token Limit Exceeded**

```
Exception: Failed to generate response: Token limit exceeded
```

**Solution**: Reduce `max_tokens` or shorten the conversation history.

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your agent code here
```

## 📖 Further Reading

- [LiteLLM Documentation](https://docs.litellm.ai/) - Multi-provider LLM library
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) - Official OpenAI documentation
- [Prompt Engineering Guide](https://www.promptingguide.ai/) - Best practices for LLM prompts
- [LangChain Documentation](https://python.langchain.com/) - Advanced agent frameworks
- [Agent Architecture Patterns](https://martinfowler.com/articles/ai-architecture.html)

## 🎓 Teaching Notes

This lab is ideal for:

- **University Course**: AI/ML programming, software engineering
- **Workshop**: Building AI-powered applications
- **Tutorial**: LLM integration and agent development
- **Interview Prep**: System design with AI components

**Estimated time**: 3-4 hours for complete implementation and testing

**Prerequisites**: Basic Python knowledge, understanding of APIs, familiarity with environment variables

---

[← Back to Main README](../../README.md) | [View Examples →](./ai_agent/agent_examples.py) | [Run Exercise →](./exercises/function_developer.py)
