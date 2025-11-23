"""
Agent class - Legacy re-export for backward compatibility.

This module re-exports Agent from agents.agent to maintain backward compatibility.
New code should import directly from agent_factory.agents.agent or agent_factory.
"""

# Re-export from agents.agent for backward compatibility
from agent_factory.agents.agent import (
    Agent,
    AgentConfig,
    AgentResult,
    AgentStatus,
    Handoff,
)

__all__ = [
    "Agent",
    "AgentConfig",
    "AgentResult",
    "AgentStatus",
    "Handoff",
]
