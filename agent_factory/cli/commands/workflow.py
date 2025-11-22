"""Workflow CLI commands."""

import typer
import json
from typing import Optional

from agent_factory.core.workflow import Workflow, WorkflowStep
from agent_factory.registry.local_registry import LocalRegistry
from agent_factory.runtime.engine import RuntimeEngine

app = typer.Typer(name="workflow", help="Manage workflows")


@app.command()
def create(
    workflow_id: str = typer.Argument(..., help="Workflow ID"),
    name: str = typer.Option(..., "--name", "-n", help="Workflow name"),
    steps_file: str = typer.Option(..., "--steps", "-s", help="Path to steps JSON file"),
):
    """Create a new workflow."""
    # Load steps from file
    with open(steps_file) as f:
        steps_data = json.load(f)
    
    steps = []
    for step_data in steps_data:
        step = WorkflowStep(
            id=step_data["id"],
            agent_id=step_data["agent_id"],
            input_mapping=step_data.get("input_mapping", {}),
            output_mapping=step_data.get("output_mapping", {}),
        )
        steps.append(step)
    
    workflow = Workflow(
        id=workflow_id,
        name=name,
        steps=steps,
    )
    
    registry = LocalRegistry()
    registry.register_workflow(workflow)
    
    runtime = RuntimeEngine()
    runtime.register_workflow(workflow)
    
    typer.echo(f"✅ Created workflow: {workflow_id}")


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
        workflow = registry.get_workflow(workflow_id)
        if workflow:
            typer.echo(f"  - {workflow_id}: {workflow.name}")
        else:
            typer.echo(f"  - {workflow_id}")


@app.command()
def run(
    workflow_id: str = typer.Argument(..., help="Workflow ID"),
    context_file: Optional[str] = typer.Option(None, "--context", "-c", help="Path to context JSON file"),
):
    """Run a workflow."""
    import json
    
    registry = LocalRegistry()
    workflow = registry.get_workflow(workflow_id)
    
    if not workflow:
        typer.echo(f"❌ Workflow not found: {workflow_id}")
        raise typer.Exit(1)
    
    # Load context
    if context_file:
        with open(context_file) as f:
            context = json.load(f)
    else:
        context = {}
    
    runtime = RuntimeEngine()
    execution_id = runtime.run_workflow(workflow_id, context)
    
    typer.echo(f"✅ Started workflow execution: {execution_id}")
    typer.echo(f"💡 Check status: agent-factory execution get {execution_id}")
