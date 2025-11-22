"""Execution API routes."""

from fastapi import APIRouter
from typing import List, Optional

from agent_factory.runtime.engine import RuntimeEngine

router = APIRouter()
runtime = RuntimeEngine()


@router.get("/{execution_id}")
def get_execution(execution_id: str):
    """Get execution by ID."""
    execution = runtime.get_execution(execution_id)
    
    if not execution:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return {
        "id": execution.id,
        "type": execution.type,
        "entity_id": execution.entity_id,
        "status": execution.status,
        "created_at": execution.created_at.isoformat(),
        "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
        "error": execution.error,
    }
