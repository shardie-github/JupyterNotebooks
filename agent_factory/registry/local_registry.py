"""
Local file-based registry for agents, tools, workflows, and blueprints.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import yaml

from agent_factory.core.agent import Agent
from agent_factory.core.tool import Tool
from agent_factory.core.workflow import Workflow
from agent_factory.core.blueprint import Blueprint


class LocalRegistry:
    """
    Local file-based registry for storing and retrieving agents, tools, workflows, and blueprints.
    
    Example:
        >>> registry = LocalRegistry("~/.agent_factory")
        >>> registry.register_agent(agent)
        >>> agent = registry.get_agent("research-assistant")
    """
    
    def __init__(self, base_path: str = "~/.agent_factory"):
        """
        Initialize local registry.
        
        Args:
            base_path: Base directory for registry storage
        """
        self.base_path = Path(base_path).expanduser()
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.base_path / "agents").mkdir(exist_ok=True)
        (self.base_path / "tools").mkdir(exist_ok=True)
        (self.base_path / "workflows").mkdir(exist_ok=True)
        (self.base_path / "blueprints").mkdir(exist_ok=True)
    
    # Agent methods
    def register_agent(self, agent: Agent) -> None:
        """Register an agent in the registry."""
        agent_file = self.base_path / "agents" / f"{agent.id}.json"
        agent_file.write_text(json.dumps(agent.to_dict(), indent=2))
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent by ID."""
        agent_file = self.base_path / "agents" / f"{agent_id}.json"
        if not agent_file.exists():
            return None
        
        data = json.loads(agent_file.read_text())
        return Agent.from_dict(data)
    
    def list_agents(self) -> List[str]:
        """List all registered agent IDs."""
        agents_dir = self.base_path / "agents"
        return [f.stem for f in agents_dir.glob("*.json")]
    
    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent from the registry."""
        agent_file = self.base_path / "agents" / f"{agent_id}.json"
        if agent_file.exists():
            agent_file.unlink()
            return True
        return False
    
    # Tool methods
    def register_tool(self, tool: Tool) -> None:
        """Register a tool in the registry."""
        tool_file = self.base_path / "tools" / f"{tool.id}.json"
        tool_file.write_text(json.dumps(tool.to_dict(), indent=2))
    
    def get_tool(self, tool_id: str) -> Optional[Tool]:
        """Get a tool by ID."""
        tool_file = self.base_path / "tools" / f"{tool_id}.json"
        if not tool_file.exists():
            return None
        
        data = json.loads(tool_file.read_text())
        # Would need full tool reconstruction - simplified for now
        return None
    
    def list_tools(self) -> List[str]:
        """List all registered tool IDs."""
        tools_dir = self.base_path / "tools"
        return [f.stem for f in tools_dir.glob("*.json")]
    
    # Workflow methods
    def register_workflow(self, workflow: Workflow) -> None:
        """Register a workflow in the registry."""
        workflow_file = self.base_path / "workflows" / f"{workflow.id}.json"
        workflow_file.write_text(json.dumps(workflow.to_dict(), indent=2))
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get a workflow by ID."""
        workflow_file = self.base_path / "workflows" / f"{workflow_id}.json"
        if not workflow_file.exists():
            return None
        
        data = json.loads(workflow_file.read_text())
        # Would need agents registry to reconstruct - simplified for now
        return None
    
    def list_workflows(self) -> List[str]:
        """List all registered workflow IDs."""
        workflows_dir = self.base_path / "workflows"
        return [f.stem for f in workflows_dir.glob("*.json")]
    
    # Blueprint methods
    def register_blueprint(self, blueprint: Blueprint) -> None:
        """Register a blueprint in the registry."""
        blueprint_dir = self.base_path / "blueprints" / blueprint.id
        blueprint_dir.mkdir(parents=True, exist_ok=True)
        
        # Save blueprint.yaml
        (blueprint_dir / "blueprint.yaml").write_text(blueprint.to_yaml())
    
    def get_blueprint(self, blueprint_id: str) -> Optional[Blueprint]:
        """Get a blueprint by ID."""
        blueprint_file = self.base_path / "blueprints" / blueprint_id / "blueprint.yaml"
        if not blueprint_file.exists():
            return None
        
        return Blueprint.from_yaml(str(blueprint_file))
    
    def list_blueprints(self) -> List[str]:
        """List all registered blueprint IDs."""
        blueprints_dir = self.base_path / "blueprints"
        return [d.name for d in blueprints_dir.iterdir() if d.is_dir()]
    
    def search(self, query: str, category: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Search registry for agents, tools, workflows, and blueprints.
        
        Args:
            query: Search query
            category: Optional category filter ("agent", "tool", "workflow", "blueprint")
            
        Returns:
            Dictionary with search results
        """
        results = {
            "agents": [],
            "tools": [],
            "workflows": [],
            "blueprints": [],
        }
        
        query_lower = query.lower()
        
        if not category or category == "agent":
            for agent_id in self.list_agents():
                agent = self.get_agent(agent_id)
                if agent and query_lower in agent.name.lower():
                    results["agents"].append(agent_id)
        
        if not category or category == "tool":
            for tool_id in self.list_tools():
                # Simplified search
                if query_lower in tool_id.lower():
                    results["tools"].append(tool_id)
        
        if not category or category == "workflow":
            for workflow_id in self.list_workflows():
                if query_lower in workflow_id.lower():
                    results["workflows"].append(workflow_id)
        
        if not category or category == "blueprint":
            for blueprint_id in self.list_blueprints():
                blueprint = self.get_blueprint(blueprint_id)
                if blueprint and query_lower in blueprint.name.lower():
                    results["blueprints"].append(blueprint_id)
        
        return results
