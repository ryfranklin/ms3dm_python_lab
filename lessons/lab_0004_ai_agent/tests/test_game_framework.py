"""Tests for the GAME framework components."""

import pytest

from ..ai_agent.game_framework import (
    Action,
    ActionRegistry,
    Agent,
    AgentFunctionCallingActionLanguage,
    AgentTextLanguage,
    Environment,
    Goal,
    Memory,
)


class TestGoal:
    """Test Goal class."""

    def test_goal_creation(self):
        """Test creating a Goal."""
        goal = Goal(priority=1, name="Test", description="Test description")
        assert goal.priority == 1
        assert goal.name == "Test"
        assert goal.description == "Test description"

    def test_goal_comparison(self):
        """Test goal priority comparison."""
        goal1 = Goal(priority=1, name="High", description="High priority")
        goal2 = Goal(priority=2, name="Low", description="Low priority")
        assert goal1 < goal2
        assert goal2 > goal1

    def test_goal_string(self):
        """Test goal string representation."""
        goal = Goal(priority=1, name="Test", description="Test description")
        assert "Goal" in str(goal)
        assert "priority=1" in str(goal)


class TestAction:
    """Test Action class."""

    def test_action_creation(self):
        """Test creating an Action."""

        def test_func():
            return "test"

        action = Action(
            name="test",
            function=test_func,
            description="Test action",
            parameters={},
            terminal=False,
        )
        assert action.name == "test"
        assert action.function == test_func
        assert action.description == "Test action"
        assert action.terminal is False

    def test_terminal_action(self):
        """Test creating a terminal action."""

        def terminate():
            return "done"

        action = Action(
            name="terminate",
            function=terminate,
            description="Terminate",
            parameters={},
            terminal=True,
        )
        assert action.terminal is True


class TestActionRegistry:
    """Test ActionRegistry class."""

    def test_registry_creation(self):
        """Test creating an ActionRegistry."""
        registry = ActionRegistry()
        assert len(registry.get_all()) == 0

    def test_register_action(self):
        """Test registering an action."""

        def test_func():
            return "test"

        registry = ActionRegistry()
        action = Action(
            name="test",
            function=test_func,
            description="Test",
            parameters={},
        )
        registry.register(action)
        assert len(registry.get_all()) == 1

    def test_get_action(self):
        """Test getting an action from registry."""

        def test_func():
            return "test"

        registry = ActionRegistry()
        action = Action(
            name="test", function=test_func, description="Test", parameters={}
        )
        registry.register(action)

        retrieved = registry.get("test")
        assert retrieved is not None
        assert retrieved.name == "test"

    def test_get_nonexistent_action(self):
        """Test getting non-existent action returns None."""
        registry = ActionRegistry()
        assert registry.get("nonexistent") is None

    def test_get_tool_specs(self):
        """Test converting actions to tool specs."""

        def test_func(x: int) -> int:
            return x * 2

        registry = ActionRegistry()
        action = Action(
            name="multiply",
            function=test_func,
            description="Multiply by 2",
            parameters={
                "type": "object",
                "properties": {"x": {"type": "integer"}},
                "required": ["x"],
            },
        )
        registry.register(action)

        tool_specs = registry.get_tool_specs()
        assert len(tool_specs) == 1
        assert tool_specs[0]["type"] == "function"
        assert tool_specs[0]["function"]["name"] == "multiply"


class TestMemory:
    """Test Memory class."""

    def test_memory_creation(self):
        """Test creating empty Memory."""
        memory = Memory()
        assert len(memory) == 0

    def test_memory_with_initial(self):
        """Test creating Memory with initial state."""
        initial = [{"role": "user", "content": "Hello"}]
        memory = Memory(initial_memory=initial)
        assert len(memory) == 1

    def test_add_memory(self):
        """Test adding a memory entry."""
        memory = Memory()
        memory.add("user_input", "Hello world")
        assert len(memory) == 1

    def test_add_memory_with_metadata(self):
        """Test adding memory with metadata."""
        memory = Memory()
        memory.add("user_input", "Hello", metadata={"timestamp": "2024-01-01"})
        assert len(memory) == 1
        memories = memory.get_memories()
        assert memories[0]["metadata"]["timestamp"] == "2024-01-01"

    def test_extend_memory(self):
        """Test extending memory with multiple entries."""
        memory = Memory()
        new_memories = [
            {"role": "user", "content": "A"},
            {"role": "assistant", "content": "B"},
        ]
        memory.extend(new_memories)
        assert len(memory) == 2

    def test_get_memories(self):
        """Test getting all memories."""
        memory = Memory()
        memory.add("type1", "content1")
        memory.add("type2", "content2")

        memories = memory.get_memories()
        assert len(memories) == 2
        assert memories[0]["content"] == "content1"

    def test_clear_memory(self):
        """Test clearing memory."""
        memory = Memory()
        memory.add("type1", "content1")
        memory.clear()
        assert len(memory) == 0


class TestEnvironment:
    """Test Environment class."""

    def test_environment_creation(self):
        """Test creating Environment."""
        env = Environment()
        assert env.config == {}

    def test_environment_with_config(self):
        """Test creating Environment with config."""
        env = Environment(working_dir=".", debug=True)
        assert env.config["working_dir"] == "."
        assert env.config["debug"] is True

    def test_update_environment(self):
        """Test updating environment config."""
        env = Environment()
        env.update(key="value")
        assert env.get("key") == "value"

    def test_get_with_default(self):
        """Test getting config with default value."""
        env = Environment()
        assert env.get("nonexistent", default="default") == "default"


class TestAgentLanguage:
    """Test AgentLanguage base class."""

    def test_format_system_prompt(self):
        """Test formatting system prompt with goals."""
        # Use concrete implementation for testing base class methods
        language = AgentFunctionCallingActionLanguage()
        goals = [
            Goal(
                priority=2,
                name="Low Priority",
                description="Low priority goal",
            ),
            Goal(
                priority=1,
                name="High Priority",
                description="High priority goal",
            ),
        ]
        prompt = language.format_system_prompt(goals)
        assert "High Priority" in prompt
        assert "Low Priority" in prompt
        assert "priority goal" in prompt

    def test_format_response_for_memory(self):
        """Test formatting response for memory storage."""
        language = AgentFunctionCallingActionLanguage()
        memory_entry = language.format_response_for_memory(
            "test_action", {"arg": "value"}
        )
        assert memory_entry["role"] == "assistant"
        assert "test_action" in memory_entry["content"]
        assert "value" in memory_entry["content"]

    def test_extract_tool_calls(self):
        """Test extracting tool calls from LLM response."""
        language = AgentFunctionCallingActionLanguage()

        # Mock LLM response with tool calls
        class MockToolCall:
            def __init__(self, name, arguments):
                self.function = type(
                    "Function", (), {"name": name, "arguments": arguments}
                )()

        class MockMessage:
            def __init__(self, tool_calls):
                self.tool_calls = tool_calls

        class MockChoice:
            def __init__(self, message):
                self.message = message

        class MockResponse:
            def __init__(self, tool_calls):
                tool = MockToolCall("test_action", '{"arg": "value"}')
                message = MockMessage([tool] if tool_calls else None)
                self.choices = [MockChoice(message)]

        # Test with tool calls
        response_with_tools = MockResponse(tool_calls=True)
        tool_calls = language.extract_tool_calls(response_with_tools)
        assert tool_calls is not None
        assert len(tool_calls) == 1
        assert tool_calls[0]["name"] == "test_action"
        assert tool_calls[0]["arguments"]["arg"] == "value"

        # Test without tool calls
        response_without_tools = MockResponse(tool_calls=False)
        tool_calls = language.extract_tool_calls(response_without_tools)
        assert tool_calls is None


class TestAgentFunctionCallingActionLanguage:
    """Test AgentFunctionCallingActionLanguage class."""

    def test_format_action(self):
        """Test formatting an action."""
        language = AgentFunctionCallingActionLanguage()
        formatted = language.format_action("test_func", {"arg1": "value"})
        assert "test_func" in formatted
        assert "value" in formatted
        # Should be valid JSON
        import json

        data = json.loads(formatted)
        assert data["tool_name"] == "test_func"
        assert data["args"]["arg1"] == "value"

    def test_parse_action(self):
        """Test parsing an action."""
        language = AgentFunctionCallingActionLanguage()
        formatted = '{"tool_name": "test_func", "args": {"arg1": "value"}}'
        name, args = language.parse_action(formatted)
        assert name == "test_func"
        assert args["arg1"] == "value"

    def test_parse_invalid_action(self):
        """Test parsing invalid action raises error."""
        language = AgentFunctionCallingActionLanguage()
        with pytest.raises(ValueError):
            language.parse_action("invalid json")

    def test_roundtrip_action(self):
        """Test formatting and parsing action maintains data integrity."""
        language = AgentFunctionCallingActionLanguage()
        original_name = "read_file"
        original_args = {"file_name": "test.txt", "encoding": "utf-8"}

        formatted = language.format_action(original_name, original_args)
        parsed_name, parsed_args = language.parse_action(formatted)

        assert parsed_name == original_name
        assert parsed_args == original_args


class TestAgentTextLanguage:
    """Test AgentTextLanguage class."""

    def test_format_action_no_args(self):
        """Test formatting action without arguments."""
        language = AgentTextLanguage()
        formatted = language.format_action("read_file", {})
        assert formatted.startswith("Action:")
        assert "read_file" in formatted

    def test_format_action_with_args(self):
        """Test formatting action with arguments."""
        language = AgentTextLanguage()
        formatted = language.format_action(
            "read_file", {"file_name": "test.txt"}
        )
        assert formatted.startswith("Action:")
        assert "read_file" in formatted
        assert "file_name=test.txt" in formatted

    def test_parse_action_simple(self):
        """Test parsing simple action."""
        language = AgentTextLanguage()
        formatted = "Action: read_file"
        name, args = language.parse_action(formatted)
        assert name == "read_file"
        assert args == {}

    def test_parse_action_with_args(self):
        """Test parsing action with arguments."""
        language = AgentTextLanguage()
        formatted = "Action: read_file with parameters: file_name=test.txt, encoding=utf-8"
        name, args = language.parse_action(formatted)
        assert name == "read_file"
        assert args["file_name"] == "test.txt"
        assert args["encoding"] == "utf-8"

    def test_parse_invalid_action(self):
        """Test parsing invalid action raises error."""
        language = AgentTextLanguage()
        with pytest.raises(ValueError):
            language.parse_action("This is not an action")

    def test_roundtrip_action(self):
        """Test formatting and parsing maintains action information."""
        language = AgentTextLanguage()
        original_name = "search_database"
        original_args = {"query": "python", "limit": "10"}

        formatted = language.format_action(original_name, original_args)
        parsed_name, parsed_args = language.parse_action(formatted)

        assert parsed_name == original_name
        # Note: args values are strings in text format, so comparison may need adjustment
        assert "python" in str(parsed_args.values())
        assert "10" in str(parsed_args.values())


class TestAgent:
    """Test Agent class."""

    def test_agent_creation(self):
        """Test creating an Agent."""

        def mock_generate(messages, tools):
            """Mock generate_response function."""

            # Return a mock response object
            class MockResponse:
                class MockChoice:
                    class MockMessage:
                        tool_calls = None
                        content = "Test response"

                    message = MockMessage()

                choices = [MockChoice()]

            return MockResponse()

        goals = [Goal(priority=1, name="Test", description="Test goal")]
        language = AgentFunctionCallingActionLanguage()
        registry = ActionRegistry()
        environment = Environment()

        agent = Agent(
            goals=goals,
            agent_language=language,
            action_registry=registry,
            generate_response=mock_generate,
            environment=environment,
        )

        assert agent.goals == goals
        assert agent.action_registry == registry
        assert agent.max_iterations == 10

    def test_goals_sorted_by_priority(self):
        """Test that goals are sorted by priority."""

        def mock_generate(messages, tools):
            class MockResponse:
                class MockChoice:
                    class MockMessage:
                        tool_calls = None
                        content = "Test response"

                    message = MockMessage()

                choices = [MockChoice()]

            return MockResponse()

        goals = [
            Goal(priority=3, name="C", description="Low priority"),
            Goal(priority=1, name="A", description="High priority"),
            Goal(priority=2, name="B", description="Medium priority"),
        ]

        agent = Agent(
            goals=goals,
            agent_language=AgentFunctionCallingActionLanguage(),
            action_registry=ActionRegistry(),
            generate_response=mock_generate,
            environment=Environment(),
        )

        # Goals should be sorted by priority
        assert agent.goals[0].name == "A"
        assert agent.goals[1].name == "B"
        assert agent.goals[2].name == "C"
