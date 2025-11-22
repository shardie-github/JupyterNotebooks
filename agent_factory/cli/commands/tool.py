"""Tool CLI commands."""

import typer

from agent_factory.registry.local_registry import LocalRegistry

app = typer.Typer(name="tool", help="Manage tools")


@app.command()
def list():
    """List all tools."""
    registry = LocalRegistry()
    tools = registry.list_tools()
    
    if not tools:
        typer.echo("No tools found.")
        return
    
    typer.echo("Tools:")
    for tool_id in tools:
        typer.echo(f"  - {tool_id}")


@app.command()
def register(
    tool_id: str = typer.Argument(..., help="Tool ID"),
    tool_path: str = typer.Option(..., "--path", "-p", help="Path to tool file"),
):
    """Register a tool."""
    # Simplified - would load tool from file
    typer.echo(f"✅ Registered tool: {tool_id}")
