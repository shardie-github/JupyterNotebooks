"""
Analytics engine for computing growth metrics and insights.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict

from agent_factory.telemetry.collector import TelemetryCollector, get_collector
from agent_factory.telemetry.model import EventType


class AnalyticsEngine:
    """
    Analytics engine for computing growth metrics and insights.
    
    Computes metrics like:
    - DAU/WAU/MAU (Daily/Weekly/Monthly Active Users)
    - Active agents/workflows per tenant
    - Blueprint installs per type
    - Conversion funnel metrics
    - Token usage & costs per tenant
    
    Example:
        >>> analytics = AnalyticsEngine()
        >>> metrics = analytics.get_growth_summary()
        >>> print(metrics["dau"])
    """
    
    def __init__(self, collector: Optional[TelemetryCollector] = None):
        """
        Initialize analytics engine.
        
        Args:
            collector: Telemetry collector instance
        """
        self.collector = collector or get_collector()
    
    def get_growth_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Get overall growth summary metrics.
        
        Args:
            start_date: Start date for metrics (defaults to 30 days ago)
            end_date: End date for metrics (defaults to now)
            
        Returns:
            Dictionary with growth metrics
        """
        if not end_date:
            end_date = datetime.utcnow()
        
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        # Get all events in the period
        events = self.collector.query_events(
            start_time=start_date,
            end_time=end_date,
            limit=10000,  # Large limit for aggregation
        )
        
        # Compute metrics
        metrics = {
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "dau": self._compute_dau(events, end_date),
            "wau": self._compute_wau(events, end_date),
            "mau": self._compute_mau(events, end_date),
            "total_tenants": self._count_unique_tenants(events),
            "total_users": self._count_unique_users(events),
            "total_agent_runs": self._count_events(events, EventType.AGENT_RUN.value),
            "total_workflow_runs": self._count_events(events, EventType.WORKFLOW_RUN.value),
            "total_blueprint_installs": self._count_events(events, EventType.BLUEPRINT_INSTALL.value),
            "total_errors": self._count_events(events, EventType.ERROR.value),
            "total_tokens_used": self._sum_tokens(events),
            "total_cost_estimate": self._sum_costs(events),
            "active_agents": self._count_unique_agents(events),
            "active_workflows": self._count_unique_workflows(events),
            "blueprint_installs_by_type": self._blueprint_installs_by_type(events),
        }
        
        return metrics
    
    def get_tenant_metrics(
        self,
        tenant_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Get metrics for a specific tenant.
        
        Args:
            tenant_id: Tenant ID
            start_date: Start date for metrics
            end_date: End date for metrics
            
        Returns:
            Dictionary with tenant-specific metrics
        """
        if not end_date:
            end_date = datetime.utcnow()
        
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        events = self.collector.query_events(
            tenant_id=tenant_id,
            start_time=start_date,
            end_time=end_date,
            limit=10000,
        )
        
        metrics = {
            "tenant_id": tenant_id,
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "total_users": self._count_unique_users(events),
            "total_agent_runs": self._count_events(events, EventType.AGENT_RUN.value),
            "total_workflow_runs": self._count_events(events, EventType.WORKFLOW_RUN.value),
            "total_blueprint_installs": self._count_events(events, EventType.BLUEPRINT_INSTALL.value),
            "total_errors": self._count_events(events, EventType.ERROR.value),
            "total_tokens_used": self._sum_tokens(events),
            "total_cost_estimate": self._sum_costs(events),
            "active_agents": self._count_unique_agents(events),
            "active_workflows": self._count_unique_workflows(events),
            "agent_runs_by_agent": self._agent_runs_by_agent(events),
            "workflow_runs_by_workflow": self._workflow_runs_by_workflow(events),
            "error_rate": self._compute_error_rate(events),
        }
        
        return metrics
    
    def get_conversion_funnel(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Compute conversion funnel metrics.
        
        Tracks: notebook → agent → blueprint → SaaS app
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Conversion funnel metrics
        """
        if not end_date:
            end_date = datetime.utcnow()
        
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        events = self.collector.query_events(
            start_time=start_date,
            end_time=end_date,
            limit=10000,
        )
        
        # Count conversions
        notebook_conversions = self._count_events(events, EventType.NOTEBOOK_CONVERTED.value)
        agents_created = self._count_unique_agents(events)
        blueprints_installed = self._count_events(events, EventType.BLUEPRINT_INSTALL.value)
        projects_created = self._count_events(events, EventType.PROJECT_CREATED.value)
        
        funnel = {
            "notebooks_converted": notebook_conversions,
            "agents_created": agents_created,
            "blueprints_installed": blueprints_installed,
            "projects_created": projects_created,
            "conversion_rates": {
                "notebook_to_agent": agents_created / notebook_conversions if notebook_conversions > 0 else 0.0,
                "agent_to_blueprint": blueprints_installed / agents_created if agents_created > 0 else 0.0,
                "blueprint_to_project": projects_created / blueprints_installed if blueprints_installed > 0 else 0.0,
            },
        }
        
        return funnel
    
    def _compute_dau(self, events: List, date: datetime) -> int:
        """Compute Daily Active Users."""
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        day_events = [
            e for e in events
            if day_start <= e.timestamp < day_end and e.user_id
        ]
        
        return len(set(e.user_id for e in day_events))
    
    def _compute_wau(self, events: List, date: datetime) -> int:
        """Compute Weekly Active Users."""
        week_start = date - timedelta(days=7)
        
        week_events = [
            e for e in events
            if week_start <= e.timestamp <= date and e.user_id
        ]
        
        return len(set(e.user_id for e in week_events))
    
    def _compute_mau(self, events: List, date: datetime) -> int:
        """Compute Monthly Active Users."""
        month_start = date - timedelta(days=30)
        
        month_events = [
            e for e in events
            if month_start <= e.timestamp <= date and e.user_id
        ]
        
        return len(set(e.user_id for e in month_events))
    
    def _count_unique_tenants(self, events: List) -> int:
        """Count unique tenants."""
        tenant_ids = {e.tenant_id for e in events if e.tenant_id}
        return len(tenant_ids)
    
    def _count_unique_users(self, events: List) -> int:
        """Count unique users."""
        user_ids = {e.user_id for e in events if e.user_id}
        return len(user_ids)
    
    def _count_events(self, events: List, event_type: str) -> int:
        """Count events of a specific type."""
        return sum(1 for e in events if e.event_type.value == event_type)
    
    def _count_unique_agents(self, events: List) -> int:
        """Count unique agents."""
        from agent_factory.telemetry.model import AgentRunEvent
        
        agent_ids = {
            e.agent_id for e in events
            if isinstance(e, AgentRunEvent) and e.agent_id
        }
        return len(agent_ids)
    
    def _count_unique_workflows(self, events: List) -> int:
        """Count unique workflows."""
        from agent_factory.telemetry.model import WorkflowRunEvent
        
        workflow_ids = {
            e.workflow_id for e in events
            if isinstance(e, WorkflowRunEvent) and e.workflow_id
        }
        return len(workflow_ids)
    
    def _sum_tokens(self, events: List) -> int:
        """Sum tokens used across events."""
        from agent_factory.telemetry.model import AgentRunEvent, WorkflowRunEvent
        
        total = 0
        for e in events:
            if isinstance(e, AgentRunEvent):
                total += e.tokens_used
            elif isinstance(e, WorkflowRunEvent):
                total += e.tokens_used
        
        return total
    
    def _sum_costs(self, events: List) -> float:
        """Sum cost estimates across events."""
        from agent_factory.telemetry.model import AgentRunEvent, WorkflowRunEvent
        
        total = 0.0
        for e in events:
            if isinstance(e, AgentRunEvent):
                total += e.cost_estimate
            elif isinstance(e, WorkflowRunEvent):
                total += e.cost_estimate
        
        return total
    
    def _blueprint_installs_by_type(self, events: List) -> Dict[str, int]:
        """Count blueprint installs by blueprint ID."""
        from agent_factory.telemetry.model import BlueprintInstallEvent
        
        counts = defaultdict(int)
        for e in events:
            if isinstance(e, BlueprintInstallEvent) and e.install_type == "install":
                blueprint_id = e.blueprint_id or "unknown"
                counts[blueprint_id] += 1
        
        return dict(counts)
    
    def _agent_runs_by_agent(self, events: List) -> Dict[str, int]:
        """Count agent runs by agent ID."""
        from agent_factory.telemetry.model import AgentRunEvent
        
        counts = defaultdict(int)
        for e in events:
            if isinstance(e, AgentRunEvent):
                agent_id = e.agent_id or "unknown"
                counts[agent_id] += 1
        
        return dict(counts)
    
    def _workflow_runs_by_workflow(self, events: List) -> Dict[str, int]:
        """Count workflow runs by workflow ID."""
        from agent_factory.telemetry.model import WorkflowRunEvent
        
        counts = defaultdict(int)
        for e in events:
            if isinstance(e, WorkflowRunEvent):
                workflow_id = e.workflow_id or "unknown"
                counts[workflow_id] += 1
        
        return dict(counts)
    
    def _compute_error_rate(self, events: List) -> float:
        """Compute error rate (errors / total events)."""
        total_events = len(events)
        if total_events == 0:
            return 0.0
        
        error_count = self._count_events(events, EventType.ERROR.value)
        return error_count / total_events


# Global analytics instance
_analytics: Optional[AnalyticsEngine] = None


def get_analytics() -> AnalyticsEngine:
    """
    Get global analytics engine instance.
    
    Returns:
        Analytics engine
    """
    global _analytics
    if _analytics is None:
        _analytics = AnalyticsEngine()
    return _analytics
