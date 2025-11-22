"""
Tool configuration schema.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any, List


@dataclass
class ToolConfig:
    """Configuration for a Tool."""
    timeout: int = 30  # seconds
    retry_attempts: int = 3
    rate_limit: Optional[int] = None  # requests per minute
    cache_enabled: bool = False
    cache_ttl: int = 3600  # seconds
    require_auth: bool = False
    auth_config: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
