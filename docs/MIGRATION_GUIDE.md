# Migration Guide: From Notebooks to Agent Factory Platform

This guide helps you migrate from the Jupyter notebook examples to using the Agent Factory Platform library.

## Overview

The Agent Factory Platform provides a production-ready Python library that extracts the patterns from the notebooks into reusable components. This guide shows you how to convert notebook code to library usage.

## Key Changes

### 1. Agent Creation

**Before (Notebook):**
```python
# Manual OpenAI SDK setup
from openai import OpenAI
client = OpenAI()
# ... complex setup code
```

**After (Library):**
```python
from agent_factory import Agent

agent = Agent(
    id="my-agent",
    name="My Agent",
    instructions="You are a helpful assistant.",
    model="gpt-4o",
)
```

### 2. Tool Creation

**Before (Notebook):**
```python
# Manual tool definition
def my_tool(param: str):
    return result

# Complex OpenAI tool schema creation
tool_schema = {
    "type": "function",
    "function": {
        "name": "my_tool",
        "description": "...",
        "parameters": {...}
    }
}
```

**After (Library):**
```python
from agent_factory import function_tool

@function_tool(name="my_tool", description="My tool")
def my_tool(param: str) -> str:
    return result

# Use directly with agent
agent = Agent(..., tools=[my_tool])
```

### 3. Memory Management

**Before (Notebook):**
```python
# Manual session management
sessions = {}
session_id = "user-123"
if session_id not in sessions:
    sessions[session_id] = []
sessions[session_id].append({"role": "user", "content": input})
```

**After (Library):**
```python
from agent_factory.core.memory import SQLiteMemoryStore

memory = SQLiteMemoryStore("sessions.db")
agent = Agent(..., memory=memory)

# Automatic session management
result = agent.run("Hello", session_id="user-123")
```

### 4. Guardrails

**Before (Notebook):**
```python
# Manual validation
def validate_input(text):
    # Custom validation logic
    if "bad_word" in text:
        return False
    return True
```

**After (Library):**
```python
from agent_factory.core.guardrails import Guardrails, ProfanityGuardrail, LengthGuardrail

guardrails = Guardrails()
guardrails.add_input_guardrail(ProfanityGuardrail())
guardrails.add_input_guardrail(LengthGuardrail(max_length=1000))

agent = Agent(..., guardrails=guardrails)
```

### 5. Multi-Agent Systems

**Before (Notebook):**
```python
# Manual handoff logic
def route_to_agent(input_text):
    if "data" in input_text:
        return data_analyst.run(input_text)
    elif "content" in input_text:
        return content_writer.run(input_text)
```

**After (Library):**
```python
from agent_factory import Agent, Handoff

# Create specialist agents
data_analyst = Agent(id="analyst", ...)
content_writer = Agent(id="writer", ...)

# Coordinator with handoff capability
coordinator = Agent(
    id="coordinator",
    instructions="Route to appropriate specialist",
    # Handoffs handled automatically
)
```

### 6. Workflows

**Before (Notebook):**
```python
# Manual workflow orchestration
def run_pipeline(input_data):
    step1_result = agent1.run(input_data)
    step2_result = agent2.run(step1_result)
    return step2_result
```

**After (Library):**
```python
from agent_factory.core.workflow import Workflow, WorkflowStep

workflow = Workflow(
    id="pipeline",
    name="Data Pipeline",
    steps=[
        WorkflowStep(id="step1", agent_id="agent1"),
        WorkflowStep(id="step2", agent_id="agent2"),
    ],
)

result = workflow.execute({"input": input_data})
```

## Step-by-Step Migration

### Step 1: Install the Library

```bash
pip install agent-factory
```

### Step 2: Set Up Environment

```bash
# Copy .env.example to .env
cp .env.example .env

# Add your API keys
echo "OPENAI_API_KEY=your-key-here" >> .env
```

### Step 3: Convert Your Notebook Cells

1. **Extract Agent Definitions**: Convert notebook agent setup to `Agent()` calls
2. **Convert Tools**: Use `@function_tool` decorator for tools
3. **Add Memory**: Use `SQLiteMemoryStore` for session management
4. **Add Guardrails**: Configure safety checks
5. **Create Workflows**: Use `Workflow` class for multi-step processes

### Step 4: Test Your Migration

```python
# Test basic agent
from agent_factory import Agent

agent = Agent(
    id="test",
    name="Test",
    instructions="You are helpful.",
)

result = agent.run("Hello!")
print(result.output)
```

### Step 5: Use CLI or API

**CLI:**
```bash
# Create agent
agent-factory agent create my-agent --name "My Agent" --instructions "..."

# Run agent
agent-factory agent run my-agent --input "Hello!"
```

**API:**
```bash
# Start API server
uvicorn agent_factory.api.main:app --reload

# Create agent via API
curl -X POST http://localhost:8000/api/v1/agents/ \
  -H "Content-Type: application/json" \
  -d '{"id": "my-agent", "name": "My Agent", "instructions": "..."}'
```

## Common Patterns

### Pattern 1: Basic Agent with Tools

```python
from agent_factory import Agent
from agent_factory.integrations.tools import calculator_tool, web_search_tool

agent = Agent(
    id="assistant",
    name="Assistant",
    instructions="You are helpful.",
    tools=[calculator_tool, web_search_tool],
)
```

### Pattern 2: Agent with Memory

```python
from agent_factory import Agent
from agent_factory.core.memory import SQLiteMemoryStore

memory = SQLiteMemoryStore("sessions.db")

agent = Agent(
    id="chatbot",
    name="Chatbot",
    instructions="You are a chatbot.",
    memory=memory,
)

# Use session_id for conversation continuity
result = agent.run("Hello", session_id="user-123")
```

### Pattern 3: Multi-Agent System

```python
from agent_factory import Agent

# Specialist agents
analyst = Agent(id="analyst", instructions="Analyze data")
writer = Agent(id="writer", instructions="Write content")

# Coordinator
coordinator = Agent(
    id="coordinator",
    instructions="Route to appropriate specialist",
)
```

### Pattern 4: Workflow Orchestration

```python
from agent_factory.core.workflow import Workflow, WorkflowStep

workflow = Workflow(
    id="research-pipeline",
    name="Research Pipeline",
    steps=[
        WorkflowStep(id="search", agent_id="searcher"),
        WorkflowStep(id="analyze", agent_id="analyzer"),
    ],
    agents_registry={"searcher": searcher_agent, "analyzer": analyzer_agent},
)

result = workflow.execute({"query": "Python async"})
```

## Benefits of Migration

1. **Production Ready**: Built-in error handling, retries, logging
2. **Composability**: Mix and match agents, tools, workflows
3. **CLI & API**: Programmatic access via command line or REST API
4. **Registry**: Discover and share components
5. **Blueprints**: Package and distribute complete solutions
6. **Observability**: Built-in metrics and tracing
7. **Scaling**: Runtime engine handles execution and scaling

## Troubleshooting

### Issue: OpenAI API Key Not Found

**Solution:**
```bash
export OPENAI_API_KEY=your-key-here
# Or add to .env file
```

### Issue: Tool Execution Fails

**Solution:** Check tool implementation and parameters:
```python
# Verify tool schema
tool = my_tool.tool
print(tool.get_schema())

# Test tool directly
result = tool.execute(param="test")
```

### Issue: Memory Not Persisting

**Solution:** Ensure session_id is consistent:
```python
# Use same session_id for conversation
session_id = "user-123"
result1 = agent.run("Hello", session_id=session_id)
result2 = agent.run("What did I say?", session_id=session_id)  # Has context
```

## Next Steps

1. **Explore Examples**: Check `examples/` directory
2. **Try Blueprints**: Install pre-built blueprints
3. **Build Custom Tools**: Create your own tool integrations
4. **Deploy**: Use Docker for production deployment

## Support

- **Documentation**: https://docs.agentfactory.io
- **GitHub**: https://github.com/agentfactory/platform
- **Discord**: [Join our community]

---

**Happy Building! 🚀**
