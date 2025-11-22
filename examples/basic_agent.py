"""
Example: Basic Agent

Refactored from Agentic_Notebook.ipynb Cell 4
"""

from agent_factory import Agent
from agent_factory.integrations.tools import calculator_tool, web_search_tool


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
        tools=[calculator_tool, web_search_tool] if calculator_tool and web_search_tool else [],
    )
    
    # Run agent
    result = agent.run("Calculate 15% tip on $87.50")
    
    print(f"Output: {result.output}")
    print(f"Status: {result.status}")
    print(f"Execution time: {result.execution_time:.2f}s")


if __name__ == "__main__":
    main()
