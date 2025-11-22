"""Workflow API routes."""

from fastapi import APIRouter
from typing import List

from agent_factory.registry.local_registry import LocalRegistry

router = APIRouter()
registry = LocalRegistry()


@router.get("/", response_model=List[str])
def list_workflows():
    """List all workflows."""
    return registry.list_workflows()
