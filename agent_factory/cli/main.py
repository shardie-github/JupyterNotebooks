"""
Main CLI entry point for Agent Factory Platform.
"""

import typer
from typing import Optional

from agent_factory.cli.commands import agent, tool, workflow, blueprint, registry, marketplace

app = typer.Typer(
    name="agent-factory",
    help="Agent Factory Platform - Build AI agents in minutes",
    add_completion=False,
)

# Add command groups
app.add_typer(agent.app, name="agent")
app.add_typer(tool.app, name="tool")
app.add_typer(workflow.app, name="workflow")
app.add_typer(blueprint.app, name="blueprint")
app.add_typer(registry.app, name="registry")
app.add_typer(marketplace.app, name="marketplace")

# Add execution commands
from agent_factory.cli.commands.execution import app as execution_app
app.add_typer(execution_app, name="execution")

# Add new command groups
from agent_factory.cli.commands import notebook, promptlog, eval, ui, saas
app.add_typer(notebook.app, name="notebook")
app.add_typer(promptlog.app, name="promptlog")
app.add_typer(eval.app, name="eval")
app.add_typer(ui.app, name="ui")
app.add_typer(saas.app, name="saas")


@app.command()
def version():
    """Show version information."""
    from agent_factory import __version__
    typer.echo(f"Agent Factory Platform v{__version__}")


@app.command()
def init(
    project_name: str = typer.Option("my_agent_project", "--name", "-n", help="Project name"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
):
    """Initialize a new Agent Factory project."""
    import os
    from pathlib import Path
    
    project_path = Path(path) if path else Path(project_name)
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Create directory structure
    (project_path / "agents").mkdir(exist_ok=True)
    (project_path / "tools").mkdir(exist_ok=True)
    (project_path / "workflows").mkdir(exist_ok=True)
    (project_path / "blueprints").mkdir(exist_ok=True)
    
    # Create .env.example
    env_example = """# Agent Factory Configuration
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Environment
ENVIRONMENT=development
"""
    (project_path / ".env.example").write_text(env_example)
    
    # Create README
    readme = f"""# {project_name}

Agent Factory project.

## Quick Start

1. Copy `.env.example` to `.env` and add your API keys
2. Create agents: `agent-factory agent create`
3. Run agents: `agent-factory agent run <agent-id>`
"""
    (project_path / "README.md").write_text(readme)
    
    typer.echo(f"✅ Project initialized at {project_path.absolute()}")


if __name__ == "__main__":
    app()
