"""
Replay agent runs with different configurations.
"""

import uuid
from typing import Dict, Optional, Any

from agent_factory.promptlog.model import Run
from agent_factory.promptlog.storage import PromptLogStorage


def replay_run(
    run_id: str,
    storage: PromptLogStorage,
    agent_config_override: Optional[Dict[str, Any]] = None,
) -> Run:
    """
    Replay a run with optional configuration overrides.
    
    Args:
        run_id: ID of run to replay
        storage: Storage backend
        agent_config_override: Optional config overrides
    
    Returns:
        New Run with replayed execution
    """
    # Get original run
    original_run = storage.get_run(run_id)
    if not original_run:
        raise ValueError(f"Run not found: {run_id}")
    
    # Create new run ID
    new_run_id = f"{run_id}-replay-{uuid.uuid4().hex[:8]}"
    
    # TODO: Actually replay via runtime engine
    # For now, return a placeholder
    new_run = Run(
        run_id=new_run_id,
        agent_id=original_run.agent_id,
        workflow_id=original_run.workflow_id,
        inputs=original_run.inputs,
        outputs=original_run.outputs,  # Would be different after replay
        status="success",
        execution_time=original_run.execution_time,
        tokens_used=original_run.tokens_used,
        cost_estimate=original_run.cost_estimate,
        metadata={
            "replayed_from": run_id,
            "config_override": agent_config_override or {},
        },
    )
    
    storage.save_run(new_run)
    return new_run
