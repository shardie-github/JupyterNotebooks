"""Marketplace CLI commands."""

import typer
from typing import Optional
from agent_factory.core.blueprint import Blueprint
from agent_factory.marketplace import publish_blueprint, search_blueprints, get_blueprint_details
from agent_factory.registry.local_registry import LocalRegistry

app = typer.Typer()
registry = LocalRegistry()


@app.command()
def publish(
    blueprint_id: str,
    public: bool = typer.Option(True, "--public/--private", help="Make blueprint public"),
    pricing: str = typer.Option("free", help="Pricing model: free, one-time, subscription"),
    price: float = typer.Option(0.0, help="Price in USD"),
):
    """Publish blueprint to marketplace."""
    blueprint = registry.get_blueprint(blueprint_id)
    
    if not blueprint:
        typer.echo(f"Blueprint {blueprint_id} not found", err=True)
        raise typer.Exit(1)
    
    try:
        result = publish_blueprint(
            blueprint=blueprint,
            publisher_id="cli-user",  # In production, get from auth
            is_public=public,
            pricing_model=pricing,
            price=price
        )
        typer.echo(f"Blueprint published: {result['id']}")
    except Exception as e:
        typer.echo(f"Failed to publish blueprint: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def search(
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Search query"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Category filter"),
    limit: int = typer.Option(20, "--limit", "-l", help="Results limit"),
):
    """Search blueprints in marketplace."""
    results = search_blueprints(
        query=query,
        category=category,
        limit=limit
    )
    
    typer.echo(f"Found {results['total']} blueprints:")
    for bp in results["blueprints"]:
        typer.echo(f"  - {bp['name']} ({bp['id']}) - Rating: {bp['rating']:.1f}")


@app.command()
def details(blueprint_id: str):
    """Get blueprint details from marketplace."""
    details = get_blueprint_details(blueprint_id)
    
    if not details:
        typer.echo(f"Blueprint {blueprint_id} not found", err=True)
        raise typer.Exit(1)
    
    typer.echo(f"Name: {details['name']}")
    typer.echo(f"Description: {details['description']}")
    typer.echo(f"Version: {details['version']}")
    typer.echo(f"Pricing: {details['pricing_model']} - ${details['price']:.2f}")
    typer.echo(f"Rating: {details['rating']:.1f} ({details['reviews_count']} reviews)")
    typer.echo(f"Downloads: {details['downloads']}")
