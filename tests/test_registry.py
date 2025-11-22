"""Tests for Registry classes."""

import pytest
import tempfile
from pathlib import Path
from agent_factory.registry.local_registry import LocalRegistry
from agent_factory.core.agent import Agent


@pytest.mark.unit
def test_local_registry_creation():
    """Test creating a local registry."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = LocalRegistry(tmpdir)
        
        assert Path(tmpdir).exists()
        assert (Path(tmpdir) / "agents").exists()
        assert (Path(tmpdir) / "tools").exists()


@pytest.mark.unit
def test_local_registry_agent_operations():
    """Test agent operations in local registry."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = LocalRegistry(tmpdir)
        
        agent = Agent(
            id="test-agent",
            name="Test Agent",
            instructions="Test",
        )
        
        # Register
        registry.register_agent(agent)
        
        # List
        agents = registry.list_agents()
        assert "test-agent" in agents
        
        # Get
        retrieved = registry.get_agent("test-agent")
        assert retrieved is not None
        assert retrieved.id == "test-agent"
        
        # Delete
        result = registry.delete_agent("test-agent")
        assert result is True
        
        # Verify deleted
        assert registry.get_agent("test-agent") is None
