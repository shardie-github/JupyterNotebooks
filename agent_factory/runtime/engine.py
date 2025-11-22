"""
Runtime engine for executing agents and workflows.
"""

from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from datetime import datetime
import uuid

from agent_factory.core.agent import Agent, AgentResult
from agent_factory.core.workflow import Workflow, WorkflowResult


@dataclass
class Execution:
    """Represents an execution instance."""
    id: str
    type: str  # "agent" or "workflow"
    entity_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RuntimeEngine:
    """
    Runtime engine for executing agents and workflows.
    
    Example:
        >>> engine = RuntimeEngine()
        >>> result = engine.run_agent(agent, "Hello")
        >>> execution = engine.get_execution(execution_id)
    """
    
    def __init__(self):
        """Initialize runtime engine."""
        self.executions: Dict[str, Execution] = {}
        self.agents_registry: Dict[str, Agent] = {}
        self.workflows_registry: Dict[str, Workflow] = {}
    
    def register_agent(self, agent: Agent) -> None:
        """Register an agent in the runtime."""
        self.agents_registry[agent.id] = agent
    
    def register_workflow(self, workflow: Workflow) -> None:
        """Register a workflow in the runtime."""
        self.workflows_registry[workflow.id] = workflow
        # Update workflow's agents registry
        workflow.agents_registry = self.agents_registry
    
    def run_agent(
        self,
        agent_id: str,
        input_text: str,
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Run an agent and return execution ID.
        
        Args:
            agent_id: Agent ID to run
            input_text: Input text
            session_id: Optional session ID
            context: Optional context
            
        Returns:
            Execution ID
        """
        agent = self.agents_registry.get(agent_id)
        if not agent:
            raise ValueError(f"Agent not found: {agent_id}")
        
        execution_id = str(uuid.uuid4())
        execution = Execution(
            id=execution_id,
            type="agent",
            entity_id=agent_id,
            status="running",
            created_at=datetime.now(),
            metadata={"input_text": input_text, "session_id": session_id, "context": context},
        )
        self.executions[execution_id] = execution
        
        try:
            result = agent.run(input_text, session_id=session_id, context=context)
            
            execution.status = "completed"
            execution.completed_at = datetime.now()
            execution.result = result
            
            return execution_id
            
        except Exception as e:
            execution.status = "error"
            execution.completed_at = datetime.now()
            execution.error = str(e)
            raise
    
    def run_workflow(
        self,
        workflow_id: str,
        context: Dict[str, Any],
    ) -> str:
        """
        Run a workflow and return execution ID.
        
        Args:
            workflow_id: Workflow ID to run
            context: Initial context
            
        Returns:
            Execution ID
        """
        workflow = self.workflows_registry.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_id}")
        
        execution_id = str(uuid.uuid4())
        execution = Execution(
            id=execution_id,
            type="workflow",
            entity_id=workflow_id,
            status="running",
            created_at=datetime.now(),
            metadata={"context": context},
        )
        self.executions[execution_id] = execution
        
        try:
            result = workflow.execute(context)
            
            execution.status = "completed"
            execution.completed_at = datetime.now()
            execution.result = result
            
            return execution_id
            
        except Exception as e:
            execution.status = "error"
            execution.completed_at = datetime.now()
            execution.error = str(e)
            raise
    
    def get_execution(self, execution_id: str) -> Optional[Execution]:
        """Get execution by ID."""
        return self.executions.get(execution_id)
    
    def list_executions(
        self,
        entity_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> List[Execution]:
        """
        List executions with optional filters.
        
        Args:
            entity_id: Filter by entity ID
            status: Filter by status
            limit: Maximum number of results
            
        Returns:
            List of executions
        """
        results = list(self.executions.values())
        
        if entity_id:
            results = [e for e in results if e.entity_id == entity_id]
        
        if status:
            results = [e for e in results if e.status == status]
        
        # Sort by created_at descending
        results.sort(key=lambda e: e.created_at, reverse=True)
        
        return results[:limit]
