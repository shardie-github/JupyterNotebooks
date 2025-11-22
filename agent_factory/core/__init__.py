"""
Core module - Legacy imports for backward compatibility.
"""

# Re-export from new locations for backward compatibility
from agent_factory.agents.agent import Agent, AgentConfig, AgentResult, AgentStatus, Handoff
from agent_factory.tools.base import Tool
from agent_factory.tools.decorator import function_tool
from agent_factory.workflows.model import Workflow, WorkflowStep, WorkflowResult, Trigger, TriggerType, Condition
from agent_factory.runtime.memory import MemoryStore, SQLiteMemoryStore

# Keep exceptions here for now
from agent_factory.core.exceptions import (
    AgentFactoryError,
    AgentError,
    AgentNotFoundError,
    AgentExecutionError,
    ToolError,
    ToolNotFoundError,
    ToolExecutionError,
    ToolValidationError,
    WorkflowError,
    WorkflowNotFoundError,
    WorkflowExecutionError,
    BlueprintError,
    BlueprintNotFoundError,
    BlueprintValidationError,
)

# Keep guardrails here for now
from agent_factory.core.guardrails import Guardrails, Guardrail, GuardrailResult

__all__ = [
    # Agents
    "Agent",
    "AgentConfig",
    "AgentResult",
    "AgentStatus",
    "Handoff",
    # Tools
    "Tool",
    "function_tool",
    # Workflows
    "Workflow",
    "WorkflowStep",
    "WorkflowResult",
    "Trigger",
    "TriggerType",
    "Condition",
    # Memory
    "MemoryStore",
    "SQLiteMemoryStore",
    # Exceptions
    "AgentFactoryError",
    "AgentError",
    "AgentNotFoundError",
    "AgentExecutionError",
    "ToolError",
    "ToolNotFoundError",
    "ToolExecutionError",
    "ToolValidationError",
    "WorkflowError",
    "WorkflowNotFoundError",
    "WorkflowExecutionError",
    "BlueprintError",
    "BlueprintNotFoundError",
    "BlueprintValidationError",
    # Guardrails
    "Guardrails",
    "Guardrail",
    "GuardrailResult",
]
