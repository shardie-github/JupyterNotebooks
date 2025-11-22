"""
OpenAI Agents SDK integration for Agent Factory Platform.
"""

import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from agent_factory.core.tool import Tool


class OpenAIAgentClient:
    """
    Client for interacting with OpenAI Agents SDK.
    
    This wraps the OpenAI SDK to provide agent execution capabilities.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def run_agent(
        self,
        instructions: str,
        input_text: str,
        model: str = "gpt-4o",
        tools: Optional[List[Tool]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run an agent using OpenAI API.
        
        Args:
            instructions: System instructions for the agent
            input_text: User input
            model: Model to use
            tools: List of tools available to the agent
            temperature: Temperature setting
            max_tokens: Maximum tokens
            context: Optional conversation context
            
        Returns:
            Dictionary with output and metadata
        """
        # Convert tools to OpenAI format
        openai_tools = []
        if tools:
            for tool in tools:
                tool_schema = tool.get_schema()
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.id,
                        "description": tool.description,
                        "parameters": tool_schema.get("parameters", {}),
                    }
                })
        
        # Build messages
        messages = [
            {"role": "system", "content": instructions}
        ]
        
        # Add context if provided
        if context and "messages" in context:
            messages.extend(context["messages"][-10:])  # Last 10 messages
        
        # Add user input
        messages.append({"role": "user", "content": input_text})
        
        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            tools=openai_tools if openai_tools else None,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        # Extract response
        message = response.choices[0].message
        output = message.content or ""
        
        # Handle tool calls if any
        tool_calls = []
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_calls.append({
                    "id": tool_call.id,
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments,
                })
        
        return {
            "output": output,
            "tool_calls": tool_calls,
            "tokens_used": response.usage.total_tokens if response.usage else 0,
            "model": model,
        }
    
    def execute_tool_call(
        self,
        tool: Tool,
        arguments: Dict[str, Any],
    ) -> Any:
        """
        Execute a tool call.
        
        Args:
            tool: Tool to execute
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        return tool.execute(**arguments)
