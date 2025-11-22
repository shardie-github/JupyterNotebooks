"""
Write agents, tools, and workflows to files.
"""

import yaml
from pathlib import Path
from typing import Dict, Any


class AgentWriter:
    """Write agent configurations to YAML files."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.agents_dir = output_dir / "agents"
        self.agents_dir.mkdir(parents=True, exist_ok=True)
    
    def write(self, agent_id: str, agent_def: Dict[str, Any]) -> Path:
        """
        Write agent configuration to YAML file.
        
        Args:
            agent_id: Agent identifier
            agent_def: Agent definition dictionary
        
        Returns:
            Path to written file
        """
        config = {
            "agent": {
                "id": agent_id,
                "name": agent_def.get("name", agent_id.replace("-", " ").title()),
                "instructions": agent_def.get("instructions", ""),
                "model": agent_def.get("model", "gpt-4o"),
                "config": {
                    "temperature": 0.7,
                    "max_tokens": 2000,
                },
                "tools": agent_def.get("tools", []),
                "metadata": {
                    "source": "notebook",
                },
            }
        }
        
        file_path = self.agents_dir / f"{agent_id}_config.yaml"
        with open(file_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
        
        return file_path


class ToolWriter:
    """Write tool implementations to Python files."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.tools_dir = output_dir / "tools"
        self.tools_dir.mkdir(parents=True, exist_ok=True)
    
    def write(self, tool_id: str, tool_def: Dict[str, Any]) -> Path:
        """
        Write tool implementation to Python file.
        
        Args:
            tool_id: Tool identifier
            tool_def: Tool definition dictionary
        
        Returns:
            Path to written file
        """
        code = tool_def.get("code", "")
        
        # If no code, generate a template
        if not code:
            code = self._generate_tool_template(tool_id, tool_def)
        
        # Ensure imports
        if "from agent_factory.tools import function_tool" not in code:
            code = "from agent_factory.tools import function_tool\n\n" + code
        
        file_path = self.tools_dir / f"{tool_id}.py"
        with open(file_path, "w") as f:
            f.write(f'"""Tool: {tool_id} - Extracted from notebook"""\n\n')
            f.write(code)
            f.write("\n")
        
        return file_path
    
    def _generate_tool_template(self, tool_id: str, tool_def: Dict[str, Any]) -> str:
        """Generate a tool template if code is missing."""
        params = tool_def.get("parameters", [])
        param_str = ", ".join(
            f"{p['name']}: {p['type']}" + (f" = None" if not p['required'] else "")
            for p in params
        )
        
        return f"""@function_tool
def {tool_id}({param_str}):
    \"\"\"{tool_def.get('description', 'Tool extracted from notebook')}\"\"\"
    # TODO: Implement tool logic
    pass
"""


class WorkflowWriter:
    """Write workflow definitions to YAML files."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.workflows_dir = output_dir / "workflows"
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
    
    def write(self, workflow_id: str, workflow_def: Dict[str, Any]) -> Path:
        """
        Write workflow definition to YAML file.
        
        Args:
            workflow_id: Workflow identifier
            workflow_def: Workflow definition dictionary
        
        Returns:
            Path to written file
        """
        config = {
            "workflow": {
                "id": workflow_id,
                "name": workflow_def.get("name", workflow_id.replace("-", " ").title()),
                "steps": workflow_def.get("steps", []),
                "metadata": {
                    "source": "notebook",
                },
            }
        }
        
        file_path = self.workflows_dir / f"{workflow_id}_workflow.yaml"
        with open(file_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
        
        return file_path
