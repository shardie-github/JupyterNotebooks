"""
Tool decorator - Convert Python functions to Tools.
"""

from typing import Optional, Callable
from agent_factory.tools.base import Tool


def function_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    **tool_kwargs
):
    """
    Decorator to convert a Python function into a Tool.
    
    Example:
        >>> @function_tool(name="calculate", description="Calculate math expressions")
        ... def calculate(expression: str) -> float:
        ...     return eval(expression)
        >>> tool = calculate  # Now it's a Tool instance
    """
    def decorator(func: Callable) -> Tool:
        tool_id = name or func.__name__
        tool_description = description or func.__doc__ or f"Tool: {func.__name__}"
        
        # Create Tool instance
        tool = Tool(
            id=tool_id,
            name=tool_id.replace("_", " ").title(),
            description=tool_description,
            implementation=func,
        )
        
        # Attach tool attributes to function
        func.tool = tool
        func.id = tool_id
        
        return tool
    
    return decorator
