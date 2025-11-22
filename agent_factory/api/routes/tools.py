"""Tool API routes."""

from fastapi import APIRouter
from typing import List

from agent_factory.registry.local_registry import LocalRegistry

router = APIRouter()
registry = LocalRegistry()


@router.get("/", response_model=List[str])
def list_tools():
    """List all tools."""
    return registry.list_tools()
