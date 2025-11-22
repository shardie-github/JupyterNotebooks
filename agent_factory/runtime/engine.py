"""
Runtime engine for executing agents and workflows with prompt logging.
"""

from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from datetime import datetime
import uuid

from agent_factory.agents.agent import Agent, AgentResult
from agent_factory.workflows.model import Workflow, WorkflowResult
from agent_factory.promptlog import SQLiteStorage, Run as RunModel
from agent_factory.telemetry.collector import get_collector


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
    Runtime engine for executing agents and workflows with integrated prompt logging.
    
    Example:
        >>> engine = RuntimeEngine()
        >>> engine.register_agent(agent)
        >>> result = engine.run_agent(agent.id, "Hello")
    """
    
    def __init__(
        self,
        prompt_log_storage: Optional[SQLiteStorage] = None,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        """
        Initialize runtime engine.
        
        Args:
            prompt_log_storage: Optional prompt log storage for logging runs
            tenant_id: Optional tenant ID for telemetry
            user_id: Optional user ID for telemetry
            project_id: Optional project ID for telemetry
        """
        self.executions: Dict[str, Execution] = {}
        self.agents_registry: Dict[str, Agent] = {}
        self.workflows_registry: Dict[str, Workflow] = {}
        self.prompt_log_storage = prompt_log_storage or SQLiteStorage()
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.project_id = project_id
        self.telemetry_collector = get_collector()
    
    def register_agent(self, agent: Agent) -> None:
        """Register an agent in the runtime."""
        self.agents_registry[agent.id] = agent
        # Wire prompt logging into agent
        if not agent.prompt_log_storage:
            agent.prompt_log_storage = self.prompt_log_storage
    
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
            
            # Log to prompt log (agent already logs internally, but we log execution too)
            self._log_execution(execution_id, agent_id, input_text, result)
            
            # Record telemetry
            self.telemetry_collector.record_agent_run(
                agent_id=agent_id,
                tenant_id=self.tenant_id,
                user_id=self.user_id,
                project_id=self.project_id,
                agent_name=getattr(agent, "name", None),
                session_id=session_id,
                status="completed" if execution.status == "completed" else "failed",
                execution_time=result.execution_time if result else 0.0,
                tokens_used=result.tokens_used if result else 0,
                cost_estimate=result.cost_estimate if result else 0.0,
                input_length=len(input_text),
                output_length=len(result.output) if result and result.output else 0,
            )
            
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
            
            # Log workflow execution
            self._log_workflow_execution(execution_id, workflow_id, context, result)
            
            # Record telemetry
            workflow = self.workflows_registry.get(workflow_id)
            self.telemetry_collector.record_workflow_run(
                workflow_id=workflow_id,
                tenant_id=self.tenant_id,
                user_id=self.user_id,
                project_id=self.project_id,
                workflow_name=getattr(workflow, "name", None) if workflow else None,
                status="completed" if execution.status == "completed" else "failed",
                execution_time=result.execution_time if result else 0.0,
                steps_completed=getattr(result, "steps_completed", 0) if result else 0,
                steps_total=getattr(result, "steps_total", 0) if result else 0,
                tokens_used=getattr(result, "tokens_used", 0) if result else 0,
                cost_estimate=getattr(result, "cost_estimate", 0.0) if result else 0.0,
            )
            
            return execution_id
            
        except Exception as e:
            execution.status = "error"
            execution.completed_at = datetime.now()
            execution.error = str(e)
            raise
    
    def _log_execution(
        self,
        execution_id: str,
        agent_id: str,
        input_text: str,
        result: AgentResult,
    ) -> None:
        """Log agent execution to prompt log."""
        try:
            run = RunModel(
                run_id=execution_id,
                agent_id=agent_id,
                inputs={"input": input_text},
                outputs={"output": result.output},
                status="success" if result.status.value == "completed" else "error",
                execution_time=result.execution_time,
                tokens_used=result.tokens_used,
                cost_estimate=0.0,
            )
            self.prompt_log_storage.save_run(run)
        except Exception:
            pass
    
    def _log_workflow_execution(
        self,
        execution_id: str,
        workflow_id: str,
        context: Dict[str, Any],
        result: WorkflowResult,
    ) -> None:
        """Log workflow execution to prompt log."""
        try:
            run = RunModel(
                run_id=execution_id,
                workflow_id=workflow_id,
                inputs=context,
                outputs=result.output,
                status="success" if result.success else "error",
                execution_time=result.execution_time,
                tokens_used=0,
                cost_estimate=0.0,
            )
            self.prompt_log_storage.save_run(run)
        except Exception:
            pass
    
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
        
        results.sort(key=lambda e: e.created_at, reverse=True)
        
        return results[:limit]
