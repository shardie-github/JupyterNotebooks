"""
Blueprint model - Packaging system for agents, tools, and workflows.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
import yaml
import json
from pathlib import Path

from agent_factory.agents.agent import Agent
from agent_factory.tools.base import Tool
from agent_factory.workflows.model import Workflow


class PricingModel(str, Enum):
    """Pricing models for blueprints."""
    FREE = "free"
    ONE_TIME = "one-time"
    SUBSCRIPTION = "subscription"
    USAGE_BASED = "usage-based"


@dataclass
class PricingInfo:
    """Pricing information for a blueprint."""
    model: PricingModel
    price: float = 0.0
    currency: str = "USD"
    period: Optional[str] = None
    usage_unit: Optional[str] = None


@dataclass
class BlueprintConfig:
    """Configuration for a blueprint."""
    dependencies: List[str] = field(default_factory=list)
    environment_variables: Dict[str, str] = field(default_factory=dict)
    required_tools: List[str] = field(default_factory=list)
    required_agents: List[str] = field(default_factory=list)


@dataclass
class BlueprintMetadata:
    """Metadata for a blueprint."""
    demo_url: str = ""
    documentation: str = ""


@dataclass
class Blueprint:
    """
    Blueprint - A packaged agent configuration.
    
    Example:
        >>> blueprint = BlueprintLoader().load("blueprints/research_assistant/blueprint.yaml")
    """
    
    id: str
    name: str
    version: str
    description: str
    author: str
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    agents: List[str] = field(default_factory=list)  # Agent IDs or paths
    tools: List[str] = field(default_factory=list)  # Tool IDs or paths
    workflows: List[str] = field(default_factory=list)  # Workflow IDs or paths
    knowledge_packs: List[str] = field(default_factory=list)  # Knowledge pack IDs
    config: BlueprintConfig = field(default_factory=BlueprintConfig)
    metadata: BlueprintMetadata = field(default_factory=BlueprintMetadata)
    pricing: PricingInfo = field(default_factory=lambda: PricingInfo(model=PricingModel.FREE))
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize blueprint to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "category": self.category,
            "tags": self.tags,
            "agents": self.agents,
            "tools": self.tools,
            "workflows": self.workflows,
            "knowledge_packs": self.knowledge_packs,
            "config": {
                "dependencies": self.config.dependencies,
                "environment_variables": self.config.environment_variables,
                "required_tools": self.config.required_tools,
                "required_agents": self.config.required_agents,
            },
            "metadata": {
                "demo_url": self.metadata.demo_url,
                "documentation": self.metadata.documentation,
            },
            "pricing": {
                "model": self.pricing.model.value,
                "price": self.pricing.price,
                "currency": self.pricing.currency,
            },
        }
    
    def to_yaml(self) -> str:
        """Serialize blueprint to YAML."""
        data = {"blueprint": self.to_dict()}
        return yaml.dump(data, default_flow_style=False, sort_keys=False)
