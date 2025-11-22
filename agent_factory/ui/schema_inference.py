"""
Infer UI schema from agent/tool definitions.
"""

from typing import Dict, Any

from agent_factory.agents.agent import Agent


def infer_ui_schema(agent: Agent) -> Dict[str, Any]:
    """
    Infer UI schema from agent definition.
    
    Args:
        agent: Agent to infer schema for
    
    Returns:
        UI schema dictionary
    """
    schema = {
        "agent_id": agent.id,
        "agent_name": agent.name,
        "inputs": [],
        "outputs": [],
    }
    
    # TODO: Infer input schema from agent tools
    # TODO: Infer output schema from agent response format
    
    return schema
