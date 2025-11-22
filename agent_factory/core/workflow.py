"""
Workflow orchestration for multi-agent systems.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable
from enum import Enum


class TriggerType(str, Enum):
    """Types of workflow triggers."""
    WEBHOOK = "webhook"
    SCHEDULE = "schedule"
    EVENT = "event"
    MANUAL = "manual"


@dataclass
class Condition:
    """Condition for workflow branching."""
    expression: str  # e.g., "$steps.search.output.count > 0"
    description: Optional[str] = None


@dataclass
class Trigger:
    """Workflow trigger definition."""
    type: TriggerType
    config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True


@dataclass
class WorkflowStep:
    """A step in a workflow."""
    id: str
    agent_id: str
    input_mapping: Dict[str, str] = field(default_factory=dict)  # Maps workflow vars to agent inputs
    output_mapping: Dict[str, str] = field(default_factory=dict)  # Maps agent outputs to workflow vars
    condition: Optional[Condition] = None
    timeout: int = 30  # seconds
    retry_attempts: int = 3


@dataclass
class WorkflowResult:
    """Result from workflow execution."""
    success: bool
    output: Dict[str, Any] = field(default_factory=dict)
    steps_executed: List[str] = field(default_factory=list)
    execution_time: float = 0.0
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class Workflow:
    """
    Workflow for orchestrating multiple agents.
    
    Example:
        >>> workflow = Workflow(
        ...     id="research-pipeline",
        ...     name="Research Pipeline",
        ...     steps=[
        ...         WorkflowStep(id="search", agent_id="research-searcher"),
        ...         WorkflowStep(id="analyze", agent_id="research-analyzer"),
        ...     ]
        ... )
        >>> result = workflow.execute({"query": "Python async"})
    """
    
    def __init__(
        self,
        id: str,
        name: str,
        steps: List[WorkflowStep],
        triggers: Optional[List[Trigger]] = None,
        branching: Optional[Dict[str, Condition]] = None,
        agents_registry: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a Workflow.
        
        Args:
            id: Unique identifier
            name: Human-readable name
            steps: List of workflow steps
            triggers: Optional list of triggers
            branching: Optional branching conditions
            agents_registry: Registry of available agents
        """
        self.id = id
        self.name = name
        self.steps = steps
        self.triggers = triggers or []
        self.branching = branching or {}
        self.agents_registry = agents_registry or {}
    
    def add_step(self, step: WorkflowStep) -> None:
        """Add a step to the workflow."""
        self.steps.append(step)
    
    def add_trigger(self, trigger: Trigger) -> None:
        """Add a trigger to the workflow."""
        self.triggers.append(trigger)
    
    def execute(
        self,
        context: Dict[str, Any],
        start_step: Optional[str] = None,
    ) -> WorkflowResult:
        """
        Execute the workflow with given context.
        
        Args:
            context: Initial context dictionary
            start_step: Optional step ID to start from
            
        Returns:
            WorkflowResult with execution results
        """
        import time
        start_time = time.time()
        
        try:
            workflow_context = context.copy()
            steps_executed = []
            
            # Determine starting step
            start_index = 0
            if start_step:
                for i, step in enumerate(self.steps):
                    if step.id == start_step:
                        start_index = i
                        break
            
            # Execute steps sequentially
            for i, step in enumerate(self.steps[start_index:], start=start_index):
                # Check condition if present
                if step.condition:
                    if not self._evaluate_condition(step.condition, workflow_context):
                        continue  # Skip this step
                
                # Get agent
                agent = self.agents_registry.get(step.agent_id)
                if not agent:
                    return WorkflowResult(
                        success=False,
                        error=f"Agent not found: {step.agent_id}",
                    )
                
                # Map inputs
                agent_input = self._map_inputs(step.input_mapping, workflow_context)
                
                # Execute agent
                agent_result = agent.run(agent_input)
                
                if agent_result.status.value == "error":
                    return WorkflowResult(
                        success=False,
                        error=f"Step {step.id} failed: {agent_result.error}",
                        steps_executed=steps_executed,
                    )
                
                # Map outputs
                step_output = self._map_outputs(step.output_mapping, agent_result.output)
                workflow_context.update(step_output)
                workflow_context[f"steps.{step.id}.output"] = agent_result.output
                
                steps_executed.append(step.id)
                
                # Check branching
                if step.id in self.branching:
                    condition = self.branching[step.id]
                    if self._evaluate_condition(condition, workflow_context):
                        # Branch to next step based on condition
                        # For now, continue to next step
                        pass
            
            execution_time = time.time() - start_time
            
            return WorkflowResult(
                success=True,
                output=workflow_context,
                steps_executed=steps_executed,
                execution_time=execution_time,
            )
            
        except Exception as e:
            return WorkflowResult(
                success=False,
                error=str(e),
                steps_executed=steps_executed if 'steps_executed' in locals() else [],
            )
    
    def _map_inputs(self, mapping: Dict[str, str], context: Dict[str, Any]) -> str:
        """Map workflow context to agent input."""
        # Simple mapping - in production, would support expressions like "$trigger.query"
        if not mapping:
            # Default: use first context value as input
            return str(next(iter(context.values())) if context else "")
        
        # Build input from mapped values
        inputs = []
        for key, value_path in mapping.items():
            # Resolve value_path from context (simplified)
            value = self._resolve_path(value_path, context)
            inputs.append(f"{key}: {value}")
        
        return "\n".join(inputs)
    
    def _map_outputs(self, mapping: Dict[str, str], output: str) -> Dict[str, Any]:
        """Map agent output to workflow context."""
        result = {}
        
        if not mapping:
            # Default: store output as "output"
            result["output"] = output
        else:
            for key, value_path in mapping.items():
                # For now, simple mapping
                result[key] = output
        
        return result
    
    def _resolve_path(self, path: str, context: Dict[str, Any]) -> Any:
        """Resolve a path expression in context."""
        # Simple implementation - in production, would support "$steps.search.output"
        if path.startswith("$"):
            # Remove $ and resolve
            path = path[1:]
            parts = path.split(".")
            value = context
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    return None
            return value
        
        return context.get(path, path)
    
    def _evaluate_condition(self, condition: Condition, context: Dict[str, Any]) -> bool:
        """Evaluate a condition expression."""
        # Simplified - in production, would use a proper expression evaluator
        expression = condition.expression
        
        # Replace context variables
        for key, value in context.items():
            expression = expression.replace(f"${key}", str(value))
        
        # Simple evaluation (unsafe - use ast.literal_eval or similar in production)
        try:
            return bool(eval(expression))
        except:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize workflow to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "steps": [
                {
                    "id": step.id,
                    "agent_id": step.agent_id,
                    "input_mapping": step.input_mapping,
                    "output_mapping": step.output_mapping,
                }
                for step in self.steps
            ],
            "triggers": [
                {
                    "type": trigger.type.value,
                    "config": trigger.config,
                }
                for trigger in self.triggers
            ],
            "branching": {
                k: {"expression": v.expression, "description": v.description}
                for k, v in self.branching.items()
            },
        }
