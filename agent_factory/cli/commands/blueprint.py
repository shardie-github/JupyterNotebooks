"""Blueprint CLI commands."""

import typer
from pathlib import Path
from typing import Optional

from agent_factory.core.blueprint import Blueprint
from agent_factory.registry.local_registry import LocalRegistry
from agent_factory.marketplace import publish_blueprint

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
def update(
    blueprint_id: str = typer.Argument(..., help="Blueprint ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Blueprint name"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Blueprint description"),
    version: Optional[str] = typer.Option(None, "--version", "-v", help="Blueprint version"),
):
    """Update a blueprint."""
    registry = LocalRegistry()
    blueprint = registry.get_blueprint(blueprint_id)
    
    if not blueprint:
        typer.echo(f"❌ Blueprint not found: {blueprint_id}")
        raise typer.Exit(1)
    
    if name:
        blueprint.name = name
    if description:
        blueprint.description = description
    if version:
        blueprint.version = version
    
    registry.register_blueprint(blueprint)
    typer.echo(f"✅ Updated blueprint: {blueprint_id}")


@app.command()
def delete(
    blueprint_id: str = typer.Argument(..., help="Blueprint ID"),
):
    """Delete a blueprint."""
    registry = LocalRegistry()
    blueprint_dir = registry.base_path / "blueprints" / blueprint_id
    
    if not blueprint_dir.exists():
        typer.echo(f"❌ Blueprint not found: {blueprint_id}")
        raise typer.Exit(1)
    
    import shutil
    shutil.rmtree(blueprint_dir)
    typer.echo(f"✅ Deleted blueprint: {blueprint_id}")


@app.command()
def validate(
    blueprint_path: str = typer.Argument(..., help="Path to blueprint.yaml"),
):
    """Validate a blueprint."""
    try:
        blueprint = Blueprint.from_yaml(blueprint_path)
        typer.echo(f"✅ Blueprint is valid: {blueprint.id}")
        typer.echo(f"   Name: {blueprint.name}")
        typer.echo(f"   Version: {blueprint.version}")
        typer.echo(f"   Agents: {len(blueprint.agents)}")
        typer.echo(f"   Tools: {len(blueprint.tools)}")
        typer.echo(f"   Workflows: {len(blueprint.workflows)}")
    except Exception as e:
        typer.echo(f"❌ Blueprint validation failed: {e}")
        raise typer.Exit(1)


@app.command()
def publish(
    blueprint_id: str = typer.Argument(..., help="Blueprint ID"),
    public: bool = typer.Option(True, "--public/--private", help="Make blueprint public"),
    pricing: str = typer.Option("free", help="Pricing model: free, one-time, subscription"),
    price: float = typer.Option(0.0, help="Price in USD"),
):
    """Publish a blueprint to marketplace."""
    registry = LocalRegistry()
    blueprint = registry.get_blueprint(blueprint_id)
    
    if not blueprint:
        typer.echo(f"❌ Blueprint not found: {blueprint_id}")
        raise typer.Exit(1)
    
    try:
        result = publish_blueprint(
            blueprint=blueprint,
            publisher_id="cli-user",  # In production, get from auth
            is_public=public,
            pricing_model=pricing,
            price=price
        )
        typer.echo(f"✅ Published blueprint: {result['id']}")
        typer.echo(f"   Status: {result['status']}")
    except Exception as e:
        typer.echo(f"❌ Publishing failed: {e}")
        raise typer.Exit(1)


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
