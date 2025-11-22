"""
CLI commands for UI generation.
"""

import typer

from agent_factory.ui import generate_ui

app = typer.Typer(name="ui", help="UI generation commands")


@app.command()
def generate(
    agent_id: str = typer.Argument(..., help="Agent ID"),
    output: str = typer.Option("./ui", "--output", "-o", help="Output directory"),
    template: str = typer.Option("react", "--template", "-t", help="Template type (react or html)"),
):
    """Generate UI for an agent."""
    try:
        generate_ui(agent_id, output, template)
        typer.echo(f"✅ UI generated at: {output}")
    except Exception as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(1)
