"""
Telemetry and analytics system for Agent Factory Platform.

Provides comprehensive tracking of:
- Agent runs
- Workflow runs
- Blueprint installations
- Error events
- Billing usage events
- Growth metrics
"""

from agent_factory.telemetry.model import (
    TelemetryEvent,
    AgentRunEvent,
    WorkflowRunEvent,
    BlueprintInstallEvent,
    ErrorEvent,
    BillingUsageEvent,
    TenantEvent,
    ProjectEvent,
)
from agent_factory.telemetry.collector import TelemetryCollector, get_collector
from agent_factory.telemetry.backends.base import TelemetryBackend
from agent_factory.telemetry.backends.sqlite import SQLiteTelemetryBackend
# PostgresTelemetryBackend imported lazily via backends.__getattr__
from agent_factory.telemetry.analytics import AnalyticsEngine, get_analytics

# Lazy import for PostgresTelemetryBackend
def __getattr__(name: str):
    """Lazy import for PostgresTelemetryBackend."""
    if name == "PostgresTelemetryBackend":
        from agent_factory.telemetry.backends import PostgresTelemetryBackend
        return PostgresTelemetryBackend
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "TelemetryEvent",
    "AgentRunEvent",
    "WorkflowRunEvent",
    "BlueprintInstallEvent",
    "ErrorEvent",
    "BillingUsageEvent",
    "TenantEvent",
    "ProjectEvent",
    "TelemetryCollector",
    "get_collector",
    "TelemetryBackend",
    "SQLiteTelemetryBackend",
    "PostgresTelemetryBackend",
    "AnalyticsEngine",
    "get_analytics",
]
