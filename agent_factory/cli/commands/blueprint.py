"""Blueprint CLI commands."""

import typer
from pathlib import Path

from agent_factory.core.blueprint import Blueprint
from agent_factory.registry.local_registry import LocalRegistry

app = typer.Typer(name="blueprint", help="Manage blueprints")


@app.command()
def install(
    blueprint_id: str = typer.Argument(..., help="Blueprint ID"),
    target_path: str = typer.Option(".", "--path", "-p", help="Installation path"),
):
    """Install a blueprint."""
    registry = LocalRegistry()
    blueprint = registry.get_blueprint(blueprint_id)
    
    if not blueprint:
        typer.echo(f"❌ Blueprint not found: {blueprint_id}")
        typer.echo("💡 Try: agent-factory blueprint search <query>")
        raise typer.Exit(1)
    
    if blueprint.install(target_path):
        typer.echo(f"✅ Installed blueprint: {blueprint_id}")
    else:
        typer.echo(f"❌ Installation failed: {blueprint_id}")
        raise typer.Exit(1)


@app.command()
def list():
    """List installed blueprints."""
    registry = LocalRegistry()
    blueprints = registry.list_blueprints()
    
    if not blueprints:
        typer.echo("No blueprints installed.")
        return
    
    typer.echo("Blueprints:")
    for blueprint_id in blueprints:
        blueprint = registry.get_blueprint(blueprint_id)
        if blueprint:
            typer.echo(f"  - {blueprint_id}: {blueprint.name} (v{blueprint.version})")


@app.command()
def create(
    blueprint_path: str = typer.Argument(..., help="Path to blueprint.yaml"),
):
    """Create a blueprint from YAML file."""
    blueprint = Blueprint.from_yaml(blueprint_path)
    
    registry = LocalRegistry()
    registry.register_blueprint(blueprint)
    
    typer.echo(f"✅ Created blueprint: {blueprint.id}")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
):
    """Search for blueprints."""
    registry = LocalRegistry()
    results = registry.search(query, category="blueprint")
    
    blueprints = results.get("blueprints", [])
    
    if not blueprints:
        typer.echo(f"No blueprints found for: {query}")
        return
    
    typer.echo(f"Found {len(blueprints)} blueprints:")
    for blueprint_id in blueprints:
        blueprint = registry.get_blueprint(blueprint_id)
        if blueprint:
            typer.echo(f"  - {blueprint_id}: {blueprint.name}")
