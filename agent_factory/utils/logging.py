"""Structured logging utilities."""

import logging
import sys
from typing import Optional


def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
) -> logging.Logger:
    """
    Set up structured logging.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        format_string: Optional custom format string
        
    Returns:
        Configured logger
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        stream=sys.stdout,
    )
    
    return logging.getLogger("agent_factory")
