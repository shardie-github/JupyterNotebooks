"""Tool API routes."""

from fastapi import APIRouter, HTTPException
from typing import List, Optional

from agent_factory.registry.local_registry import LocalRegistry

router = APIRouter()
registry = LocalRegistry()


@router.get("/", response_model=List[str])
def list_tools():
    """List all tools."""
    return registry.list_tools()


@router.get("/{tool_id}")
def get_tool(tool_id: str):
    """Get tool by ID."""
    tool = registry.get_tool(tool_id)
    
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    return tool.to_dict()


@router.post("/{tool_id}/test")
def test_tool(tool_id: str, params: dict):
    """Test a tool with given parameters."""
    tool = registry.get_tool(tool_id)
    
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    try:
        result = tool.execute(**params)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
