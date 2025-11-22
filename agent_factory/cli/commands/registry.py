"""Registry CLI commands."""

import typer

from agent_factory.registry.local_registry import LocalRegistry

app = typer.Typer(name="registry", help="Manage registry")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    category: str = typer.Option(None, "--category", "-c", help="Category filter"),
):
    """Search the registry."""
    registry = LocalRegistry()
    results = registry.search(query, category=category)
    
    typer.echo(f"Search results for: {query}")
    
    if results.get("agents"):
        typer.echo(f"\nAgents ({len(results['agents'])}):")
        for agent_id in results["agents"]:
            typer.echo(f"  - {agent_id}")
    
    if results.get("tools"):
        typer.echo(f"\nTools ({len(results['tools'])}):")
        for tool_id in results["tools"]:
            typer.echo(f"  - {tool_id}")
    
    if results.get("workflows"):
        typer.echo(f"\nWorkflows ({len(results['workflows'])}):")
        for workflow_id in results["workflows"]:
            typer.echo(f"  - {workflow_id}")
    
    if results.get("blueprints"):
        typer.echo(f"\nBlueprints ({len(results['blueprints'])}):")
        for blueprint_id in results["blueprints"]:
            typer.echo(f"  - {blueprint_id}")
