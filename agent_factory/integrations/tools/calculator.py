"""Calculator tool for mathematical operations."""

from agent_factory.tools.decorator import function_tool
import math


@function_tool(
    name="calculator",
    description="Perform mathematical calculations"
)
def calculator(expression: str) -> float:
    """
    Calculate a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        Calculation result
    """
    # Safe evaluation - only allow math operations
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names.update({
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
    })
    
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")


# The decorator returns a Tool instance, so calculator is already a Tool
calculator_tool = calculator
