"""Registry system for agents, tools, workflows, and blueprints."""

from agent_factory.registry.local_registry import LocalRegistry
from agent_factory.registry.remote_registry import RemoteRegistry

__all__ = ["LocalRegistry", "RemoteRegistry"]
