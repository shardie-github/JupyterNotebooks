# Agent Factory Platform - Examples Gallery

## Table of Contents

1. [Basic Agent](#basic-agent)
2. [Agent with Tools](#agent-with-tools)
3. [Multi-Agent System](#multi-agent-system)
4. [Workflow Example](#workflow-example)
5. [Custom Blueprint](#custom-blueprint)
6. [Marketplace Integration](#marketplace-integration)
7. [Enterprise Use Cases](#enterprise-use-cases)

## Basic Agent

### Simple Chat Agent

```python
from agent_factory.core.agent import Agent

# Create agent
agent = Agent(
    id="chat-agent",
    name="Chat Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4o"
)

# Run agent
result = agent.run("What is Python?")
print(result.output)
```

### Session-Based Conversation

```python
from agent_factory.core.agent import Agent

agent = Agent(
    id="conversation-agent",
    name="Conversation Agent",
    instructions="You are a friendly assistant.",
    model="gpt-4o"
)

# Start conversation
session_id = "user-123"
result1 = agent.run("Hello!", session_id=session_id)
print(result1.output)

# Continue conversation
result2 = agent.run("What did I just say?", session_id=session_id)
print(result2.output)
```

## Agent with Tools

### Web Search Agent

```python
from agent_factory.core.agent import Agent
from agent_factory.integrations.tools.web_search import web_search

# Create agent with web search tool
agent = Agent(
    id="research-agent",
    name="Research Assistant",
    instructions="You are a research assistant. Use web_search to find information.",
    model="gpt-4o",
    tools=[web_search]
)

# Run agent with tool usage
result = agent.run("What are the latest developments in AI?")
print(result.output)
```

### Calculator Agent

```python
from agent_factory.core.agent import Agent
from agent_factory.integrations.tools.calculator import calculator

agent = Agent(
    id="math-agent",
    name="Math Assistant",
    instructions="You are a math assistant. Use calculator for computations.",
    model="gpt-4o",
    tools=[calculator]
)

result = agent.run("What is 123 * 456?")
print(result.output)
```

## Multi-Agent System

### Customer Support System

```python
from agent_factory.core.agent import Agent

# Classifier agent
classifier = Agent(
    id="classifier",
    name="Request Classifier",
    instructions="Classify customer requests into: support, sales, technical",
    model="gpt-4o"
)

# Support agent
support_agent = Agent(
    id="support",
    name="Support Agent",
    instructions="You are a customer support agent.",
    model="gpt-4o"
)

# Sales agent
sales_agent = Agent(
    id="sales",
    name="Sales Agent",
    instructions="You are a sales agent.",
    model="gpt-4o"
)

# Route request
request = "I want to buy your product"
classification = classifier.run(request)

if "sales" in classification.output.lower():
    response = sales_agent.run(request)
elif "support" in classification.output.lower():
    response = support_agent.run(request)
else:
    response = support_agent.run(request)

print(response.output)
```

## Workflow Example

### E-commerce Order Processing

```python
from agent_factory.core.workflow import Workflow, Step

workflow = Workflow(
    id="order-processing",
    name="Order Processing Workflow",
    steps=[
        Step(
            id="validate",
            agent_id="validator-agent",
            input_mapping={"order": "input"}
        ),
        Step(
            id="process-payment",
            agent_id="payment-agent",
            condition="validate.status == 'valid'",
            input_mapping={"order": "validate.order"}
        ),
        Step(
            id="fulfill",
            agent_id="fulfillment-agent",
            condition="process-payment.status == 'paid'",
            input_mapping={"order": "process-payment.order"}
        ),
        Step(
            id="notify",
            agent_id="notification-agent",
            condition="fulfill.status == 'shipped'",
            input_mapping={"order": "fulfill.order"}
        )
    ]
)

# Run workflow
result = workflow.run({"order": {"id": "123", "items": [...]}})
print(result.output)
```

## Custom Blueprint

### Creating a Blueprint

```python
from agent_factory.core.blueprint import Blueprint
from agent_factory.core.agent import Agent

# Create blueprint
blueprint = Blueprint(
    id="support-bot-pro",
    name="Support Bot Pro",
    description="Advanced customer support agent",
    version="1.0.0",
    agents=[
        Agent(
            id="support-agent",
            name="Support Agent",
            instructions="You are a professional customer support agent.",
            model="gpt-4o"
        )
    ],
    tools=[],
    workflows=[],
    pricing_model="subscription",
    price=29.99
)

# Save blueprint
blueprint.save("blueprints/support-bot-pro/blueprint.yaml")
```

### Installing Blueprint

```bash
agent-factory blueprint install support-bot-pro
```

## Marketplace Integration

### Publishing Blueprint

```python
from agent_factory.marketplace import publish_blueprint
from agent_factory.core.blueprint import Blueprint

blueprint = Blueprint.load("blueprints/my-blueprint/blueprint.yaml")

result = publish_blueprint(
    blueprint=blueprint,
    publisher_id="user-123",
    is_public=True,
    pricing_model="one-time",
    price=49.99
)

print(f"Published: {result['id']}")
```

### Searching Marketplace

```python
from agent_factory.marketplace import search_blueprints

results = search_blueprints(
    query="customer support",
    min_rating=4.0,
    limit=10
)

for bp in results["blueprints"]:
    print(f"{bp['name']} - Rating: {bp['rating']}")
```

## Enterprise Use Cases

### Multi-Tenant System

```python
from agent_factory.enterprise.multitenancy import create_tenant, check_quota

# Create tenant
tenant = create_tenant(
    name="Acme Corp",
    slug="acme-corp",
    plan="enterprise"
)

# Check quota before creating agent
if check_quota(tenant["id"], "agents", requested_count=1):
    # Create agent
    agent = Agent(...)
else:
    print("Quota exceeded")
```

### Webhook Integration

```python
from agent_factory.enterprise.webhooks import register_webhook, trigger_webhook

# Register webhook
webhook = register_webhook(
    url="https://example.com/webhook",
    events=["agent.execution.completed", "workflow.completed"],
    tenant_id="tenant-123"
)

# Trigger webhook (automatically done by system)
# Or manually:
await trigger_webhook(
    event_type="agent.execution.completed",
    payload={"agent_id": "agent-123", "status": "completed"},
    tenant_id="tenant-123"
)
```

### Compliance - Data Export

```python
from agent_factory.enterprise.compliance import export_user_data

# Export user data for GDPR
data = export_user_data("user-123")
print(json.dumps(data, indent=2))
```

## Advanced Examples

### Custom Tool with Validation

```python
from agent_factory.core.tool import function_tool
from pydantic import BaseModel, Field

class WeatherRequest(BaseModel):
    location: str = Field(..., description="City name")
    units: str = Field("celsius", description="Temperature units")

@function_tool
def get_weather(request: WeatherRequest) -> str:
    """Get weather for a location."""
    # Implementation
    return f"Weather in {request.location}: Sunny, 22°C"

# Use tool
result = get_weather(WeatherRequest(location="San Francisco"))
```

### Async Agent Execution

```python
import asyncio
from agent_factory.core.agent import Agent

async def run_agents_parallel():
    agent1 = Agent(id="agent1", name="Agent 1", instructions="...", model="gpt-4o")
    agent2 = Agent(id="agent2", name="Agent 2", instructions="...", model="gpt-4o")
    
    results = await asyncio.gather(
        agent1.run_async("Task 1"),
        agent2.run_async("Task 2")
    )
    
    return results

results = asyncio.run(run_agents_parallel())
```

## Best Practices

1. **Error Handling**: Always wrap agent calls in try-except
2. **Session Management**: Use session IDs for conversations
3. **Tool Validation**: Validate tool inputs before execution
4. **Resource Cleanup**: Clean up resources after use
5. **Logging**: Log important operations for debugging

## More Examples

See the `examples/` directory for complete working examples:
- `basic_agent.py` - Basic agent usage
- `multi_agent_system.py` - Multi-agent coordination
- `customer_support_bot.py` - Customer support use case
