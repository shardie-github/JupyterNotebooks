# Agent Factory Platform - API Reference

## REST API

Base URL: `http://localhost:8000/api/v1`

### Authentication

Currently, the API does not require authentication for development. In production, add API key authentication.

### Agents

#### Create Agent

```http
POST /api/v1/agents/
Content-Type: application/json

{
  "id": "my-agent",
  "name": "My Agent",
  "instructions": "You are a helpful assistant.",
  "model": "gpt-4o"
}
```

#### List Agents

```http
GET /api/v1/agents/
```

#### Get Agent

```http
GET /api/v1/agents/{agent_id}
```

#### Run Agent

```http
POST /api/v1/agents/{agent_id}/run
Content-Type: application/json

{
  "input_text": "Hello!",
  "session_id": "optional-session-id",
  "context": {}
}
```

#### Delete Agent

```http
DELETE /api/v1/agents/{agent_id}
```

### Tools

#### List Tools

```http
GET /api/v1/tools/
```

#### Get Tool

```http
GET /api/v1/tools/{tool_id}
```

#### Test Tool

```http
POST /api/v1/tools/{tool_id}/test
Content-Type: application/json

{
  "param1": "value1",
  "param2": "value2"
}
```

### Workflows

#### Create Workflow

```http
POST /api/v1/workflows/
Content-Type: application/json

{
  "id": "my-workflow",
  "name": "My Workflow",
  "steps": [
    {
      "id": "step1",
      "agent_id": "agent1",
      "input_mapping": {},
      "output_mapping": {}
    }
  ]
}
```

#### List Workflows

```http
GET /api/v1/workflows/
```

#### Get Workflow

```http
GET /api/v1/workflows/{workflow_id}
```

#### Run Workflow

```http
POST /api/v1/workflows/{workflow_id}/run
Content-Type: application/json

{
  "context": {
    "input": "value"
  }
}
```

### Blueprints

#### List Blueprints

```http
GET /api/v1/blueprints/
```

#### Get Blueprint

```http
GET /api/v1/blueprints/{blueprint_id}
```

### Executions

#### Get Execution

```http
GET /api/v1/executions/{execution_id}
```

## Python API

### Agent

```python
from agent_factory import Agent

# Create agent
agent = Agent(
    id="my-agent",
    name="My Agent",
    instructions="You are helpful.",
    model="gpt-4o",
    tools=[tool1, tool2],
)

# Run agent
result = agent.run("Hello!", session_id="session-123")

# Access result
print(result.output)
print(result.status)
print(result.execution_time)
```

### Tool

```python
from agent_factory import function_tool

@function_tool(name="my_tool", description="My tool")
def my_tool(param: str) -> str:
    return f"Processed: {param}"

# Use with agent
agent = Agent(..., tools=[my_tool])
```

### Workflow

```python
from agent_factory.core.workflow import Workflow, WorkflowStep

workflow = Workflow(
    id="my-workflow",
    name="My Workflow",
    steps=[
        WorkflowStep(id="step1", agent_id="agent1"),
        WorkflowStep(id="step2", agent_id="agent2"),
    ],
    agents_registry={"agent1": agent1, "agent2": agent2},
)

result = workflow.execute({"input": "value"})
```

### Blueprint

```python
from agent_factory.core.blueprint import Blueprint

# Load blueprint
blueprint = Blueprint.from_yaml("blueprint.yaml")

# Install blueprint
blueprint.install("./my_project")

# Package blueprint
blueprint.package("./output")
```

### Registry

```python
from agent_factory.registry.local_registry import LocalRegistry

registry = LocalRegistry()

# Register agent
registry.register_agent(agent)

# Get agent
agent = registry.get_agent("agent-id")

# Search
results = registry.search("query", category="agent")
```

### Runtime Engine

```python
from agent_factory.runtime.engine import RuntimeEngine

runtime = RuntimeEngine()

# Register agent
runtime.register_agent(agent)

# Run agent
execution_id = runtime.run_agent("agent-id", "input text")

# Get execution
execution = runtime.get_execution(execution_id)
```

## CLI Commands

### Agents

```bash
# Create agent
agent-factory agent create my-agent --name "My Agent" --instructions "..."

# List agents
agent-factory agent list

# Run agent
agent-factory agent run my-agent --input "Hello!"

# Delete agent
agent-factory agent delete my-agent
```

### Tools

```bash
# List tools
agent-factory tool list

# Register tool
agent-factory tool register my-tool --path tool.json

# Test tool
agent-factory tool test my-tool --params '{"param": "value"}'
```

### Workflows

```bash
# Create workflow
agent-factory workflow create my-workflow --name "My Workflow" --steps steps.json

# List workflows
agent-factory workflow list

# Run workflow
agent-factory workflow run my-workflow --context context.json
```

### Blueprints

```bash
# Install blueprint
agent-factory blueprint install support-bot-pro

# List blueprints
agent-factory blueprint list

# Search blueprints
agent-factory blueprint search "support"

# Create blueprint
agent-factory blueprint create blueprint.yaml
```

### Registry

```bash
# Search registry
agent-factory registry search "query" --category agent
```

## Error Handling

All API endpoints return standard HTTP status codes:

- `200 OK`: Success
- `201 Created`: Resource created
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error responses include a `detail` field with error message:

```json
{
  "detail": "Agent not found"
}
```
