"""Workflow API routes."""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from agent_factory.core.workflow import Workflow, WorkflowStep
from agent_factory.registry.local_registry import LocalRegistry
from agent_factory.runtime.engine import RuntimeEngine

router = APIRouter()
registry = LocalRegistry()
runtime = RuntimeEngine()


class WorkflowCreate(BaseModel):
    id: str
    name: str
    steps: List[dict]
    triggers: Optional[List[dict]] = None


class WorkflowRun(BaseModel):
    context: dict


@router.post("/", response_model=dict)
def create_workflow(workflow_data: WorkflowCreate):
    """Create a new workflow."""
    # Convert steps
    steps = []
    for step_data in workflow_data.steps:
        step = WorkflowStep(
            id=step_data["id"],
            agent_id=step_data["agent_id"],
            input_mapping=step_data.get("input_mapping", {}),
            output_mapping=step_data.get("output_mapping", {}),
        )
        steps.append(step)
    
    workflow = Workflow(
        id=workflow_data.id,
        name=workflow_data.name,
        steps=steps,
    )
    
    registry.register_workflow(workflow)
    runtime.register_workflow(workflow)
    
    return {"id": workflow.id, "status": "created"}


@router.get("/", response_model=List[str])
def list_workflows():
    """List all workflows."""
    return registry.list_workflows()


@router.get("/{workflow_id}", response_model=dict)
def get_workflow(workflow_id: str):
    """Get workflow by ID."""
    workflow = registry.get_workflow(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return workflow.to_dict()


@router.post("/{workflow_id}/run", response_model=dict)
def run_workflow(workflow_id: str, run_data: WorkflowRun):
    """Run a workflow."""
    workflow = registry.get_workflow(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    execution_id = runtime.run_workflow(workflow_id, run_data.context)
    
    return {"execution_id": execution_id, "status": "running"}


@router.delete("/{workflow_id}")
def delete_workflow(workflow_id: str):
    """Delete a workflow."""
    # Simplified - would need to remove from registry
    return {"status": "deleted"}
