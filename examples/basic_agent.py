"""
Example: Basic Agent

Refactored from Agentic_Notebook.ipynb Cell 4
"""

from agent_factory import Agent, function_tool


@function_tool(name="calculate", description="Calculate mathematical expressions")
def calculate(expression: str) -> float:
    """Safely evaluate mathematical expressions."""
    allowed = set('0123456789+-*/(). ')
    if not all(c in allowed for c in expression):
        raise ValueError('Invalid characters in expression')
    
    try:
        return float(eval(expression))
    except Exception as e:
        raise ValueError(f'Cannot evaluate: {e}')


@function_tool(name="search_web", description="Search the web for information")
def search_web(query: str, max_results: int = 5) -> list:
    """Search the web for information."""
    # Mock implementation - replace with real API
    return [
        {
            'title': f'Result {i+1} for: {query}',
            'url': f'https://example.com/result{i+1}',
            'snippet': f'Information about {query}...'
        }
        for i in range(min(max_results, 3))
    ]


def main():
    """Create and run a basic agent."""
    # Create agent
    agent = Agent(
        id="general-assistant",
        name="General Assistant",
        instructions="""
        You are a helpful, friendly assistant.
        Provide clear, accurate, and concise responses.
        When you don't know something, admit it honestly.
        """,
        model="gpt-4o-mini",
        tools=[calculate, search_web],
    )
    
    # Run agent
    result = agent.run("Calculate 15% tip on $87.50")
    
    print(f"Output: {result.output}")
    print(f"Status: {result.status}")
    print(f"Execution time: {result.execution_time:.2f}s")


if __name__ == "__main__":
    main()
