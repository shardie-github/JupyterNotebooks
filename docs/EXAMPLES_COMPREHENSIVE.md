# Agent Factory Platform - Comprehensive Examples

## Table of Contents

1. [Basic Agent](#basic-agent)
2. [Agent with Tools](#agent-with-tools)
3. [Multi-Agent Workflow](#multi-agent-workflow)
4. [Custom Tools](#custom-tools)
5. [Knowledge Packs](#knowledge-packs)
6. [Blueprint Creation](#blueprint-creation)
7. [API Usage](#api-usage)
8. [CLI Usage](#cli-usage)
9. [Error Handling](#error-handling)
10. [Production Patterns](#production-patterns)

---

## Basic Agent

### Simple Agent

```python
from agent_factory import Agent

# Create a simple agent
agent = Agent(
    id="greeting-agent",
    name="Greeting Agent",
    instructions="You are a friendly assistant that greets users warmly.",
    model="gpt-4o"
)

# Run the agent
result = agent.run("Hello!")
print(result.output)
```

### Agent with Configuration

```python
from agent_factory import Agent, AgentConfig

config = AgentConfig(
    model="gpt-4o",
    temperature=0.7,
    max_tokens=2000,
    timeout=30,
    retry_attempts=3
)

agent = Agent(
    id="configured-agent",
    name="Configured Agent",
    instructions="You are a helpful assistant.",
    config=config
)

result = agent.run("What is Python?")
print(f"Output: {result.output}")
print(f"Tokens used: {result.tokens_used}")
print(f"Execution time: {result.execution_time}s")
```

---

## Agent with Tools

### Calculator Tool

```python
from agent_factory import Agent, function_tool

@function_tool(
    name="calculator",
    description="Perform mathematical calculations"
)
def calculate(expression: str) -> float:
    """Calculate a mathematical expression safely."""
    from agent_factory.utils.safe_evaluator import safe_evaluate
    return float(safe_evaluate(expression))

# Create agent with tool
agent = Agent(
    id="calculator-agent",
    name="Calculator Agent",
    instructions="You are a helpful calculator assistant.",
    tools=[calculate]
)

result = agent.run("What's 15% tip on $87.50?")
print(result.output)
```

### Multiple Tools

```python
from agent_factory import Agent, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    # Implementation here
    return f"Weather in {city}: Sunny, 72°F"

@function_tool
def get_time(timezone: str = "UTC") -> str:
    """Get current time in timezone."""
    from datetime import datetime
    return datetime.now().isoformat()

agent = Agent(
    id="multi-tool-agent",
    name="Multi-Tool Agent",
    instructions="You help with weather and time queries.",
    tools=[get_weather, get_time]
)

result = agent.run("What's the weather in New York and what time is it?")
print(result.output)
```

---

## Multi-Agent Workflow

### Sequential Workflow

```python
from agent_factory import Agent
from agent_factory.workflows.model import Workflow, WorkflowStep

# Create agents
researcher = Agent(
    id="researcher",
    name="Researcher",
    instructions="You research topics and provide summaries."
)

writer = Agent(
    id="writer",
    name="Writer",
    instructions="You write articles based on research."
)

# Create workflow
workflow = Workflow(
    id="research-write",
    name="Research and Write",
    steps=[
        WorkflowStep(
            id="research",
            agent_id="researcher",
            input_mapping={"query": "$inputs.topic"}
        ),
        WorkflowStep(
            id="write",
            agent_id="writer",
            input_mapping={"research": "$steps.research.output"}
        )
    ]
)

# Execute workflow
result = workflow.execute({"topic": "Python async programming"})
print(result.output)
```

---

## Custom Tools

### Advanced Tool

```python
from agent_factory.tools.base import Tool
from typing import Dict, Any

class DatabaseQueryTool(Tool):
    """Tool for querying databases."""
    
    def __init__(self):
        super().__init__(
            id="db_query",
            name="Database Query",
            description="Execute safe database queries",
            implementation=self._execute_query
        )
    
    def _execute_query(self, query: str, params: Dict[str, Any] = None) -> list:
        """Execute a parameterized database query."""
        # Implementation with SQLAlchemy
        from agent_factory.database.session import Session
        with Session() as session:
            result = session.execute(query, params or {})
            return [dict(row) for row in result]
        
        return []

# Use custom tool
db_tool = DatabaseQueryTool()
agent = Agent(
    id="db-agent",
    name="Database Agent",
    instructions="You help query databases safely.",
    tools=[db_tool]
)
```

---

## Knowledge Packs

### Attach Knowledge Pack

```python
from agent_factory import Agent
from agent_factory.knowledge import KnowledgePack

# Load knowledge pack
knowledge_pack = KnowledgePack.load("academic-research")

# Create agent with knowledge
agent = Agent(
    id="research-agent",
    name="Research Agent",
    instructions="You are a research assistant with access to academic knowledge.",
    knowledge_pack=knowledge_pack
)

result = agent.run("What are the latest findings on neural networks?")
print(result.output)
```

---

## Blueprint Creation

### Create Blueprint

```python
from agent_factory.blueprints.model import Blueprint, BlueprintMetadata

blueprint = Blueprint(
    id="customer-support",
    name="Customer Support Bot",
    version="1.0.0",
    description="AI-powered customer support agent",
    agents=["support-agent"],
    tools=["knowledge-base-search", "ticket-creator"],
    metadata=BlueprintMetadata(
        author="Agent Factory Team",
        category="customer-support",
        tags=["support", "customer-service"]
    )
)

# Save blueprint
blueprint.save("blueprints/customer_support/blueprint.yaml")
```

---

## API Usage

### Python SDK

```python
from agent_factory.sdk.client import AgentFactoryClient

client = AgentFactoryClient(api_key="your-api-key")

# Create agent
agent = client.agents.create(
    id="api-agent",
    name="API Agent",
    instructions="You are a helpful assistant."
)

# Run agent
result = client.agents.run(agent_id="api-agent", input_text="Hello!")
print(result.output)
```

### REST API

```bash
# Create agent
curl -X POST http://localhost:8000/api/v1/agents/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "id": "api-agent",
    "name": "API Agent",
    "instructions": "You are a helpful assistant."
  }'

# Run agent
curl -X POST http://localhost:8000/api/v1/agents/api-agent/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "input_text": "Hello!"
  }'
```

---

## CLI Usage

### Create Agent

```bash
agent-factory agent create my-agent \
  --name "My Agent" \
  --instructions "You are a helpful assistant."
```

### Run Agent

```bash
agent-factory agent run my-agent --input "What is Python?"
```

### List Agents

```bash
agent-factory agent list
```

---

## Error Handling

### Try-Except Pattern

```python
from agent_factory import Agent
from agent_factory.core.exceptions import AgentExecutionError

agent = Agent(
    id="error-handling-agent",
    name="Error Handling Agent",
    instructions="You are a helpful assistant."
)

try:
    result = agent.run("Hello!")
    print(result.output)
except AgentExecutionError as e:
    print(f"Agent execution failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Error Handling with Retries

```python
import time
from agent_factory.core.exceptions import AgentExecutionError

def run_with_retry(agent, input_text, max_retries=3):
    """Run agent with retry logic."""
    for attempt in range(max_retries):
        try:
            return agent.run(input_text)
        except AgentExecutionError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
    return None
```

---

## Production Patterns

### With Circuit Breaker

```python
from agent_factory import Agent
from agent_factory.security.circuit_breaker import get_circuit_breaker

agent = Agent(
    id="production-agent",
    name="Production Agent",
    instructions="You are a helpful assistant."
)

# Circuit breaker is automatically applied to LLM calls
result = agent.run("Hello!")
```

### With Logging

```python
import logging
from agent_factory import Agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

agent = Agent(
    id="logged-agent",
    name="Logged Agent",
    instructions="You are a helpful assistant."
)

logger.info("Running agent")
result = agent.run("Hello!")
logger.info(f"Agent completed: {result.status}")
```

### With Monitoring

```python
from agent_factory import Agent
from agent_factory.telemetry.collector import get_collector

telemetry = get_collector()

agent = Agent(
    id="monitored-agent",
    name="Monitored Agent",
    instructions="You are a helpful assistant."
)

result = agent.run("Hello!")

# Metrics are automatically recorded
# Check /api/v1/telemetry/metrics for stats
```

---

## Advanced Patterns

### Agent Handoff

```python
from agent_factory import Agent

specialist = Agent(
    id="specialist",
    name="Specialist Agent",
    instructions="You are a specialist in advanced topics."
)

generalist = Agent(
    id="generalist",
    name="Generalist Agent",
    instructions="You handle general queries and hand off to specialists."
)

# Handoff pattern
result = generalist.run("Complex technical question")
if needs_specialist(result):
    handoff = generalist.handoff(
        to=specialist,
        context={"question": result.output},
        reason="Requires specialist knowledge"
    )
    final_result = specialist.run(handoff.context["question"])
```

### Session Management

```python
from agent_factory import Agent
from agent_factory.runtime.memory import SQLiteMemoryStore

memory = SQLiteMemoryStore("sessions.db")

agent = Agent(
    id="session-agent",
    name="Session Agent",
    instructions="You maintain conversation context.",
    memory=memory
)

session_id = "user-123"

# First message
result1 = agent.run("My name is Alice", session_id=session_id)

# Second message (has context)
result2 = agent.run("What's my name?", session_id=session_id)
# Agent remembers: "Alice"
```

---

**Last Updated**: 2024-01-XX  
**Version**: 0.1.0
