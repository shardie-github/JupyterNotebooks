"""Blueprint API routes."""

from fastapi import APIRouter, HTTPException
from typing import List

from agent_factory.registry.local_registry import LocalRegistry

router = APIRouter()
registry = LocalRegistry()


@router.get("/", response_model=List[str])
def list_blueprints():
    """List all blueprints."""
    return registry.list_blueprints()


@router.get("/{blueprint_id}")
def get_blueprint(blueprint_id: str):
    """Get blueprint by ID."""
    blueprint = registry.get_blueprint(blueprint_id)
    
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    
    return blueprint.to_dict()
