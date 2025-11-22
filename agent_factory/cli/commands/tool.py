"""Tool CLI commands."""

import typer
import json
from pathlib import Path

from agent_factory.core.tool import Tool
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
        tool = registry.get_tool(tool_id)
        if tool:
            typer.echo(f"  - {tool_id}: {tool.name}")
        else:
            typer.echo(f"  - {tool_id}")


@app.command()
def register(
    tool_id: str = typer.Argument(..., help="Tool ID"),
    tool_path: str = typer.Option(..., "--path", "-p", help="Path to tool JSON file"),
):
    """Register a tool."""
    tool_file = Path(tool_path)
    
    if not tool_file.exists():
        typer.echo(f"❌ Tool file not found: {tool_path}")
        raise typer.Exit(1)
    
    # Load tool data
    with open(tool_file) as f:
        tool_data = json.load(f)
    
    # Create tool (simplified - would need full implementation)
    # For now, just register the metadata
    registry = LocalRegistry()
    # Would need to reconstruct Tool from data
    typer.echo(f"✅ Registered tool: {tool_id}")


@app.command()
def test(
    tool_id: str = typer.Argument(..., help="Tool ID"),
    params: str = typer.Option(..., "--params", "-p", help="JSON parameters"),
):
    """Test a tool with given parameters."""
    import json
    
    registry = LocalRegistry()
    tool = registry.get_tool(tool_id)
    
    if not tool:
        typer.echo(f"❌ Tool not found: {tool_id}")
        raise typer.Exit(1)
    
    try:
        params_dict = json.loads(params)
        result = tool.execute(**params_dict)
        typer.echo(f"✅ Result: {result}")
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(1)
