"""
Telemetry data models for tracking platform usage and growth.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Any
from enum import Enum


class EventType(str, Enum):
    """Telemetry event types."""
    AGENT_RUN = "agent_run"
    WORKFLOW_RUN = "workflow_run"
    BLUEPRINT_INSTALL = "blueprint_install"
    BLUEPRINT_UNINSTALL = "blueprint_uninstall"
    ERROR = "error"
    BILLING_USAGE = "billing_usage"
    TENANT_CREATED = "tenant_created"
    TENANT_UPDATED = "tenant_updated"
    PROJECT_CREATED = "project_created"
    PROJECT_UPDATED = "project_updated"
    EVAL_RUN = "eval_run"
    AUTOTUNE_RUN = "autotune_run"
    NOTEBOOK_CONVERTED = "notebook_converted"


@dataclass
class TelemetryEvent:
    """
    Base telemetry event.
    
    All telemetry events inherit from this base class.
    """
    event_id: str
    event_type: EventType
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "metadata": self.metadata,
        }


@dataclass(kw_only=True)
class AgentRunEvent(TelemetryEvent):
    """Telemetry event for agent execution."""
    agent_id: str  # Required field
    agent_name: Optional[str] = None
    session_id: Optional[str] = None
    status: str = "completed"  # completed, failed, timeout
    execution_time: float = 0.0
    tokens_used: int = 0
    cost_estimate: float = 0.0
    input_length: int = 0
    output_length: int = 0
    
    def __post_init__(self):
        """Set event type."""
        self.event_type = EventType.AGENT_RUN
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        base = super().to_dict()
        base.update({
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "session_id": self.session_id,
            "status": self.status,
            "execution_time": self.execution_time,
            "tokens_used": self.tokens_used,
            "cost_estimate": self.cost_estimate,
            "input_length": self.input_length,
            "output_length": self.output_length,
        })
        return base


@dataclass(kw_only=True)
class WorkflowRunEvent(TelemetryEvent):
    """Telemetry event for workflow execution."""
    workflow_id: str  # Required field
    workflow_name: Optional[str] = None
    status: str = "completed"  # completed, failed, timeout
    execution_time: float = 0.0
    steps_completed: int = 0
    steps_total: int = 0
    tokens_used: int = 0
    cost_estimate: float = 0.0
    
    def __post_init__(self):
        """Set event type."""
        self.event_type = EventType.WORKFLOW_RUN
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        base = super().to_dict()
        base.update({
            "workflow_id": self.workflow_id,
            "workflow_name": self.workflow_name,
            "status": self.status,
            "execution_time": self.execution_time,
            "steps_completed": self.steps_completed,
            "steps_total": self.steps_total,
            "tokens_used": self.tokens_used,
            "cost_estimate": self.cost_estimate,
        })
        return base


@dataclass(kw_only=True)
class BlueprintInstallEvent(TelemetryEvent):
    """Telemetry event for blueprint installation."""
    blueprint_id: str  # Required field
    blueprint_name: Optional[str] = None
    blueprint_version: Optional[str] = None
    install_type: str = "install"  # install, uninstall
    
    def __post_init__(self):
        """Set event type."""
        self.event_type = EventType.BLUEPRINT_INSTALL if self.install_type == "install" else EventType.BLUEPRINT_UNINSTALL
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        base = super().to_dict()
        base.update({
            "blueprint_id": self.blueprint_id,
            "blueprint_name": self.blueprint_name,
            "blueprint_version": self.blueprint_version,
            "install_type": self.install_type,
        })
        return base


@dataclass(kw_only=True)
class ErrorEvent(TelemetryEvent):
    """Telemetry event for errors."""
    error_type: str  # Required field
    error_message: str  # Required field
    resource_type: Optional[str] = None  # agent, workflow, blueprint, etc.
    resource_id: Optional[str] = None
    stack_trace: Optional[str] = None
    
    def __post_init__(self):
        """Set event type."""
        self.event_type = EventType.ERROR
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        base = super().to_dict()
        base.update({
            "error_type": self.error_type,
            "error_message": self.error_message,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "stack_trace": self.stack_trace,
        })
        return base


@dataclass(kw_only=True)
class BillingUsageEvent(TelemetryEvent):
    """Telemetry event for billing usage tracking."""
    billing_unit: str  # Required field
    quantity: float  # Required field
    unit_price: float = 0.0
    total_cost: float = 0.0
    currency: str = "USD"
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    
    def __post_init__(self):
        """Set event type."""
        self.event_type = EventType.BILLING_USAGE
        if self.total_cost == 0.0 and self.quantity > 0:
            self.total_cost = self.quantity * self.unit_price
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        base = super().to_dict()
        base.update({
            "billing_unit": self.billing_unit,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_cost": self.total_cost,
            "currency": self.currency,
            "period_start": self.period_start.isoformat() if self.period_start else None,
            "period_end": self.period_end.isoformat() if self.period_end else None,
        })
        return base


@dataclass
class TenantEvent(TelemetryEvent):
    """Telemetry event for tenant lifecycle."""
    tenant_name: Optional[str] = None
    tenant_slug: Optional[str] = None
    plan: Optional[str] = None
    action: str = "created"  # created, updated, deleted
    
    def __post_init__(self):
        """Set event type."""
        if self.action == "created":
            self.event_type = EventType.TENANT_CREATED
        elif self.action == "updated":
            self.event_type = EventType.TENANT_UPDATED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        base = super().to_dict()
        base.update({
            "tenant_name": self.tenant_name,
            "tenant_slug": self.tenant_slug,
            "plan": self.plan,
            "action": self.action,
        })
        return base


@dataclass
class ProjectEvent(TelemetryEvent):
    """Telemetry event for project/app lifecycle."""
    project_name: Optional[str] = None
    project_type: Optional[str] = None  # saas_app, blueprint_deployment, etc.
    action: str = "created"  # created, updated, deleted
    
    def __post_init__(self):
        """Set event type."""
        if self.action == "created":
            self.event_type = EventType.PROJECT_CREATED
        elif self.action == "updated":
            self.event_type = EventType.PROJECT_UPDATED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        base = super().to_dict()
        base.update({
            "project_name": self.project_name,
            "project_type": self.project_type,
            "action": self.action,
        })
        return base
