"""
Base telemetry backend interface.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from agent_factory.telemetry.model import TelemetryEvent


class TelemetryBackend(ABC):
    """
    Abstract base class for telemetry storage backends.
    
    Implementations can use SQLite, Postgres, S3, or any other storage.
    """
    
    @abstractmethod
    def store_event(self, event: TelemetryEvent) -> None:
        """
        Store a telemetry event.
        
        Args:
            event: Telemetry event to store
        """
        pass
    
    @abstractmethod
    def query_events(
        self,
        event_type: Optional[str] = None,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
        project_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[TelemetryEvent]:
        """
        Query telemetry events.
        
        Args:
            event_type: Filter by event type
            tenant_id: Filter by tenant ID
            user_id: Filter by user ID
            project_id: Filter by project ID
            start_time: Start time filter
            end_time: End time filter
            limit: Maximum number of results
            
        Returns:
            List of telemetry events
        """
        pass
