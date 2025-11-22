"""
Generate UI from agent schemas.
"""

from pathlib import Path
from typing import Optional

from agent_factory.agents.agent import Agent


def generate_ui(
    agent_id: str,
    output_dir: str,
    template: str = "react",
) -> None:
    """
    Generate UI for an agent.
    
    Args:
        agent_id: Agent ID
        output_dir: Output directory
        template: Template type ("react" or "html")
    
    Returns:
        None (writes files to output_dir)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # TODO: Load agent and infer schema
    # agent = load_agent(agent_id)
    # schema = infer_ui_schema(agent)
    
    # TODO: Generate UI files based on template
    if template == "html":
        _generate_html_ui(output_path)
    elif template == "react":
        _generate_react_ui(output_path)
    else:
        raise ValueError(f"Unsupported template: {template}")


def _generate_html_ui(output_path: Path) -> None:
    """Generate simple HTML UI."""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Agent UI</title>
</head>
<body>
    <h1>Agent Interface</h1>
    <form id="agent-form">
        <input type="text" id="input" placeholder="Enter your query">
        <button type="submit">Submit</button>
    </form>
    <div id="output"></div>
    <script>
        // TODO: Add API integration
    </script>
</body>
</html>
"""
    (output_path / "index.html").write_text(html_content)


def _generate_react_ui(output_path: Path) -> None:
    """Generate React UI (placeholder)."""
    # TODO: Generate React components
    readme = """# React UI

This is a placeholder for React UI generation.

TODO: Implement React template generation.
"""
    (output_path / "README.md").write_text(readme)
