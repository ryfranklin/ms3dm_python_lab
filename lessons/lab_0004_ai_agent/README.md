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

### 4. **Interactive Exercises** (`exercises/`)

- Hands-on function development
- Step-by-step agent interaction
- Real-world coding scenarios

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

### Exercise 2: Custom Agent Personality

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

### Exercise 3: Code Review Agent

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
