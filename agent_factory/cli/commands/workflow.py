"""Workflow CLI commands."""

import typer

from agent_factory.registry.local_registry import LocalRegistry

app = typer.Typer(name="workflow", help="Manage workflows")


@app.command()
def list():
    """List all workflows."""
    registry = LocalRegistry()
    workflows = registry.list_workflows()
    
    if not workflows:
        typer.echo("No workflows found.")
        return
    
    typer.echo("Workflows:")
    for workflow_id in workflows:
        typer.echo(f"  - {workflow_id}")
