"""
Evaluation data models.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class Scenario:
    """
    Evaluation scenario.
    
    Example:
        >>> scenario = Scenario(
        ...     id="tip-calculation",
        ...     name="Tip Calculation",
        ...     inputs={"amount": 100, "tip_percent": 15},
        ...     expected_outputs={"result": 15.0},
        ... )
    """
    id: str
    name: str
    inputs: Dict[str, Any]
    expected_outputs: Optional[Dict[str, Any]] = None
    expected_behavior: Optional[str] = None  # Natural language description
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """
    Result of evaluating an agent on a scenario.
    
    Example:
        >>> result = EvaluationResult(
        ...     scenario_id="tip-calculation",
        ...     agent_id="calculator-agent",
        ...     success=True,
        ...     accuracy=1.0,
        ...     latency=0.5,
        ...     tokens_used=50,
        ...     cost_estimate=0.001,
        ... )
    """
    scenario_id: str
    agent_id: str
    success: bool
    accuracy: Optional[float] = None  # 0.0 to 1.0, if expected_outputs provided
    latency: float = 0.0
    tokens_used: int = 0
    cost_estimate: float = 0.0
    error: Optional[str] = None
    output: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkSuite:
    """
    Collection of evaluation scenarios.
    
    Example:
        >>> suite = BenchmarkSuite(
        ...     id="math-basics",
        ...     name="Basic Math Operations",
        ...     scenarios=[scenario1, scenario2],
        ...     metrics=["accuracy", "latency", "cost"],
        ... )
    """
    id: str
    name: str
    scenarios: List[Scenario]
    metrics: List[str] = field(default_factory=lambda: ["accuracy", "latency", "cost", "error_rate"])
    metadata: Dict[str, Any] = field(default_factory=dict)
