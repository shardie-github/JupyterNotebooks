"""CLI commands for metrics and analytics."""

import typer
from datetime import datetime, timedelta
from typing import Optional

from agent_factory.telemetry.analytics import get_analytics

app = typer.Typer()


@app.command()
def summary(
    days: int = typer.Option(30, "--days", "-d", help="Number of days to analyze"),
):
    """
    Show growth metrics summary.
    
    Example:
        agent-factory metrics summary --days 30
    """
    analytics = get_analytics()
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    metrics = analytics.get_growth_summary(
        start_date=start_date,
        end_date=end_date,
    )
    
    typer.echo("\n📊 Growth Metrics Summary")
    typer.echo("=" * 50)
    typer.echo(f"Period: {start_date.date()} to {end_date.date()}")
    typer.echo(f"\n👥 Users:")
    typer.echo(f"  Daily Active Users (DAU): {metrics.get('dau', 0)}")
    typer.echo(f"  Weekly Active Users (WAU): {metrics.get('wau', 0)}")
    typer.echo(f"  Monthly Active Users (MAU): {metrics.get('mau', 0)}")
    typer.echo(f"  Total Tenants: {metrics.get('total_tenants', 0)}")
    typer.echo(f"\n🚀 Activity:")
    typer.echo(f"  Agent Runs: {metrics.get('total_agent_runs', 0)}")
    typer.echo(f"  Workflow Runs: {metrics.get('total_workflow_runs', 0)}")
    typer.echo(f"  Blueprint Installs: {metrics.get('total_blueprint_installs', 0)}")
    typer.echo(f"  Errors: {metrics.get('total_errors', 0)}")
    typer.echo(f"\n💰 Usage:")
    typer.echo(f"  Tokens Used: {metrics.get('total_tokens_used', 0):,}")
    typer.echo(f"  Estimated Cost: ${metrics.get('total_cost_estimate', 0.0):.2f}")
    typer.echo(f"\n📈 Resources:")
    typer.echo(f"  Active Agents: {metrics.get('active_agents', 0)}")
    typer.echo(f"  Active Workflows: {metrics.get('active_workflows', 0)}")


@app.command()
def tenant(
    tenant_id: str = typer.Argument(..., help="Tenant ID"),
    days: int = typer.Option(30, "--days", "-d", help="Number of days to analyze"),
):
    """
    Show metrics for a specific tenant.
    
    Example:
        agent-factory metrics tenant tenant-123 --days 7
    """
    analytics = get_analytics()
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    metrics = analytics.get_tenant_metrics(
        tenant_id=tenant_id,
        start_date=start_date,
        end_date=end_date,
    )
    
    typer.echo(f"\n📊 Metrics for Tenant: {tenant_id}")
    typer.echo("=" * 50)
    typer.echo(f"Period: {start_date.date()} to {end_date.date()}")
    typer.echo(f"\n👥 Users: {metrics.get('total_users', 0)}")
    typer.echo(f"\n🚀 Activity:")
    typer.echo(f"  Agent Runs: {metrics.get('total_agent_runs', 0)}")
    typer.echo(f"  Workflow Runs: {metrics.get('total_workflow_runs', 0)}")
    typer.echo(f"  Blueprint Installs: {metrics.get('total_blueprint_installs', 0)}")
    typer.echo(f"  Errors: {metrics.get('total_errors', 0)}")
    typer.echo(f"  Error Rate: {metrics.get('error_rate', 0.0):.2%}")
    typer.echo(f"\n💰 Usage:")
    typer.echo(f"  Tokens Used: {metrics.get('total_tokens_used', 0):,}")
    typer.echo(f"  Estimated Cost: ${metrics.get('total_cost_estimate', 0.0):.2f}")
    typer.echo(f"\n📈 Resources:")
    typer.echo(f"  Active Agents: {metrics.get('active_agents', 0)}")
    typer.echo(f"  Active Workflows: {metrics.get('active_workflows', 0)}")
    
    # Show top agents
    agent_runs = metrics.get("agent_runs_by_agent", {})
    if agent_runs:
        typer.echo(f"\n🔝 Top Agents:")
        sorted_agents = sorted(agent_runs.items(), key=lambda x: x[1], reverse=True)[:5]
        for agent_id, count in sorted_agents:
            typer.echo(f"  {agent_id}: {count} runs")


@app.command()
def funnel(
    days: int = typer.Option(30, "--days", "-d", help="Number of days to analyze"),
):
    """
    Show conversion funnel metrics.
    
    Example:
        agent-factory metrics funnel --days 30
    """
    analytics = get_analytics()
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    funnel = analytics.get_conversion_funnel(
        start_date=start_date,
        end_date=end_date,
    )
    
    typer.echo("\n🔄 Conversion Funnel")
    typer.echo("=" * 50)
    typer.echo(f"Period: {start_date.date()} to {end_date.date()}")
    typer.echo(f"\n📝 Notebooks Converted: {funnel.get('notebooks_converted', 0)}")
    typer.echo(f"🤖 Agents Created: {funnel.get('agents_created', 0)}")
    typer.echo(f"📦 Blueprints Installed: {funnel.get('blueprints_installed', 0)}")
    typer.echo(f"🚀 Projects Created: {funnel.get('projects_created', 0)}")
    
    conversion_rates = funnel.get("conversion_rates", {})
    typer.echo(f"\n📊 Conversion Rates:")
    typer.echo(f"  Notebook → Agent: {conversion_rates.get('notebook_to_agent', 0.0):.2%}")
    typer.echo(f"  Agent → Blueprint: {conversion_rates.get('agent_to_blueprint', 0.0):.2%}")
    typer.echo(f"  Blueprint → Project: {conversion_rates.get('blueprint_to_project', 0.0):.2%}")
