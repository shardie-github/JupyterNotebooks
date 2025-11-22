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
from agent_factory.telemetry.backends.postgres import PostgresTelemetryBackend
from agent_factory.telemetry.analytics import AnalyticsEngine, get_analytics

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
