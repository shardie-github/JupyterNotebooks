# Agent Factory Platform - User Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating Your First Agent](#creating-your-first-agent)
3. [Working with Tools](#working-with-tools)
4. [Building Workflows](#building-workflows)
5. [Using Blueprints](#using-blueprints)
6. [Marketplace](#marketplace)
7. [API Usage](#api-usage)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

## Getting Started

### Installation

```bash
pip install agent-factory
```

### Configuration

Create a `.env` file in your project directory:

```env
OPENAI_API_KEY=your-api-key-here
ANTHROPIC_API_KEY=your-api-key-here
ENVIRONMENT=development
```

### Initialize Project

```bash
agent-factory init my-project
cd my-project
```

## Creating Your First Agent

### Using the CLI

```bash
# Create an agent
agent-factory agent create \
  --id "my-agent" \
  --name "Customer Support Agent" \
  --instructions "You are a helpful customer support agent."

# Run the agent
agent-factory agent run my-agent --input "Hello, I need help"
```

### Using Python

```python
from agent_factory.core.agent import Agent

# Create agent
agent = Agent(
    id="my-agent",
    name="Customer Support Agent",
    instructions="You are a helpful customer support agent.",
    model="gpt-4o"
)

# Run agent
result = agent.run("Hello, I need help")
print(result.output)
```

## Working with Tools

### Creating Custom Tools

```python
from agent_factory.core.tool import function_tool

@function_tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    # Your implementation
    return f"Weather in {location}: Sunny, 72°F"

# Register tool
from agent_factory.registry.local_registry import LocalRegistry
registry = LocalRegistry()
registry.register_tool(get_weather)
```

### Using Pre-built Tools

```python
from agent_factory.integrations.tools import web_search, calculator, file_io

# Use web search
results = web_search("Python best practices")

# Use calculator
result = calculator("2 + 2")

# File operations
content = file_io.read_file("data.txt")
file_io.write_file("output.txt", "Hello World")
```

## Building Workflows

### Creating a Workflow

```python
from agent_factory.core.workflow import Workflow, Step

workflow = Workflow(
    id="support-workflow",
    name="Customer Support Workflow",
    steps=[
        Step(
            id="classify",
            agent_id="classifier-agent",
            input_mapping={"user_message": "input"}
        ),
        Step(
            id="respond",
            agent_id="support-agent",
            condition="classify.category == 'support'",
            input_mapping={"message": "classify.output"}
        )
    ]
)
```

### Running Workflows

```bash
agent-factory workflow run support-workflow --input '{"user_message": "I need help"}'
```

## Using Blueprints

### Installing Blueprints

```bash
# Search for blueprints
agent-factory blueprint search --query "customer support"

# Install blueprint
agent-factory blueprint install support-bot-pro
```

### Creating Blueprints

```bash
agent-factory blueprint create my-blueprint \
  --name "My Custom Blueprint" \
  --description "A custom blueprint for my use case"
```

## Marketplace

### Publishing Blueprints

```bash
agent-factory marketplace publish my-blueprint \
  --public \
  --pricing one-time \
  --price 29.99
```

### Searching Marketplace

```bash
agent-factory marketplace search --query "research assistant"
agent-factory marketplace details research-assistant-pro
```

## API Usage

### Authentication

```python
import requests

# Get access token
response = requests.post("https://api.agentfactory.io/auth/login", json={
    "email": "user@example.com",
    "password": "password"
})
token = response.json()["access_token"]

# Use token in requests
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("https://api.agentfactory.io/api/v1/agents", headers=headers)
```

### Creating Agents via API

```python
import requests

response = requests.post(
    "https://api.agentfactory.io/api/v1/agents",
    headers=headers,
    json={
        "id": "api-agent",
        "name": "API Agent",
        "instructions": "You are a helpful assistant.",
        "model": "gpt-4o"
    }
)
```

## Best Practices

### 1. Agent Design

- **Clear Instructions**: Write specific, clear instructions for your agents
- **Context Management**: Use session IDs for multi-turn conversations
- **Error Handling**: Always handle errors gracefully

### 2. Tool Design

- **Descriptive Names**: Use clear, descriptive function names
- **Type Hints**: Always include type hints for parameters
- **Documentation**: Add docstrings explaining tool purpose

### 3. Workflow Design

- **Modular Steps**: Break workflows into logical steps
- **Error Recovery**: Include error handling steps
- **Testing**: Test each step independently

### 4. Performance

- **Caching**: Use caching for expensive operations
- **Async Execution**: Use async for I/O-bound operations
- **Rate Limiting**: Respect API rate limits

## Troubleshooting

### Common Issues

**Issue**: Agent not responding
- Check API keys are set correctly
- Verify agent instructions are clear
- Check network connectivity

**Issue**: Tool not found
- Ensure tool is registered
- Check tool name spelling
- Verify tool is in correct registry

**Issue**: Workflow failing
- Check step conditions
- Verify input mappings
- Review execution logs

### Getting Help

- **Documentation**: https://docs.agentfactory.io
- **GitHub Issues**: https://github.com/agentfactory/platform/issues
- **Discord**: https://discord.gg/agentfactory
