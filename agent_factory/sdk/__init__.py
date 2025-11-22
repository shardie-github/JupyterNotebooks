"""
Agent Factory Platform Python SDK.

Provides a clean Python interface for programmatic control of the Agent Factory Platform.

Example:
    >>> from agent_factory.sdk import Client
    >>> client = Client(api_key="your-api-key", base_url="https://api.agentfactory.io")
    >>> result = client.run_agent("my-agent", "Hello!")
    >>> print(result["output"])
"""

from agent_factory.sdk.client import Client

__all__ = ["Client"]
