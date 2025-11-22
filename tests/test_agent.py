"""Tests for Agent class."""

import pytest
from agent_factory.core.agent import Agent, AgentConfig, AgentStatus


def test_agent_creation():
    """Test creating an agent."""
    agent = Agent(
        id="test-agent",
        name="Test Agent",
        instructions="You are a test agent.",
    )
    
    assert agent.id == "test-agent"
    assert agent.name == "Test Agent"
    assert agent.instructions == "You are a test agent."
    assert agent.model == "gpt-4o"


def test_agent_with_tools():
    """Test agent with tools."""
    from agent_factory.core.tool import Tool
    
    def dummy_tool(x: str) -> str:
        return f"Processed: {x}"
    
    tool = Tool(
        id="dummy-tool",
        name="Dummy Tool",
        description="A dummy tool",
        implementation=dummy_tool,
    )
    
    agent = Agent(
        id="test-agent",
        name="Test Agent",
        instructions="Test",
        tools=[tool],
    )
    
    assert len(agent.tools) == 1
    assert agent.tools[0].id == "dummy-tool"


def test_agent_add_tool():
    """Test adding a tool to an agent."""
    from agent_factory.core.tool import Tool
    
    def dummy_tool(x: str) -> str:
        return f"Processed: {x}"
    
    tool = Tool(
        id="dummy-tool",
        name="Dummy Tool",
        description="A dummy tool",
        implementation=dummy_tool,
    )
    
    agent = Agent(
        id="test-agent",
        name="Test Agent",
        instructions="Test",
    )
    
    agent.add_tool(tool)
    assert len(agent.tools) == 1


def test_agent_serialization():
    """Test agent serialization."""
    agent = Agent(
        id="test-agent",
        name="Test Agent",
        instructions="Test",
    )
    
    data = agent.to_dict()
    
    assert data["id"] == "test-agent"
    assert data["name"] == "Test Agent"
    assert data["instructions"] == "Test"


def test_agent_deserialization():
    """Test agent deserialization."""
    data = {
        "id": "test-agent",
        "name": "Test Agent",
        "instructions": "Test",
        "model": "gpt-4o",
        "tools": [],
        "config": {
            "temperature": 0.7,
            "max_tokens": 2000,
        },
        "metadata": {},
    }
    
    agent = Agent.from_dict(data)
    
    assert agent.id == "test-agent"
    assert agent.name == "Test Agent"
    assert agent.instructions == "Test"
