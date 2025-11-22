# Quick Start Guide

Get started with Agent Factory Platform in 5 minutes.

## Installation

```bash
pip install agent-factory
```

## Setup

1. **Set API Key**

```bash
export OPENAI_API_KEY=your-key-here
```

Or create a `.env` file:

```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

## Your First Agent

### Python

```python
from agent_factory import Agent
from agent_factory.integrations.tools import calculator_tool

# Create agent
agent = Agent(
    id="my-first-agent",
    name="My First Agent",
    instructions="You are a helpful assistant.",
    tools=[calculator_tool],
)

# Run agent
result = agent.run("Calculate 15% tip on $87.50")
print(result.output)
```

### CLI

```bash
# Create agent
agent-factory agent create my-agent \
  --name "My Agent" \
  --instructions "You are helpful."

# Run agent
agent-factory agent run my-agent --input "Hello!"
```

### API

```bash
# Start API server
uvicorn agent_factory.api.main:app --reload

# Create agent
curl -X POST http://localhost:8000/api/v1/agents/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "my-agent",
    "name": "My Agent",
    "instructions": "You are helpful."
  }'

# Run agent
curl -X POST http://localhost:8000/api/v1/agents/my-agent/run \
  -H "Content-Type: application/json" \
  -d '{"input_text": "Hello!"}'
```

## Next Steps

1. **Add Tools**: Use pre-built tools or create your own
2. **Add Memory**: Enable conversation history
3. **Create Workflows**: Orchestrate multiple agents
4. **Install Blueprints**: Use pre-built solutions
5. **Deploy**: Use Docker for production

See [Full Documentation](README.md) for more details.
