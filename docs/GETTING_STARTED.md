# Getting Started with Agent Factory Platform

> **From Notebook to Production Agent in 5 Steps**

This guide walks you through converting a Jupyter notebook into a production-ready agent, attaching knowledge packs, running evaluations, and generating a UI.

## Prerequisites

- Python 3.8+
- OpenAI API key (optional, for full LLM integration)
- pip installed

## Installation

```bash
pip install agent-factory
```

Or install from source:
```bash
git clone https://github.com/agentfactory/platform.git
cd platform
pip install -e ".[dev]"
```

## Quick Start: Your First Agent

Let's create a minimal working agent:

```python
from agent_factory import Agent, function_tool

# Step 1: Create a tool
@function_tool(name="greet", description="Greet someone by name")
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}! Nice to meet you."

# Step 2: Create an agent with the tool
agent = Agent(
    id="greeting-agent",
    name="Greeting Agent",
    instructions="You are a friendly assistant that greets people.",
    tools=[greet],
)

# Step 3: Run the agent
result = agent.run("Please greet Alice")
print(result.output)  # Will use LLM if API key set, otherwise mock response
```

Run this example:
```bash
python examples/minimal_working_example.py
```

## Step 2: Convert Notebook to Agent

Use the notebook converter to extract agents, tools, and workflows:

```bash
agent-factory notebook convert Agentic_Notebook.ipynb \
  --agent-name research-assistant \
  --create-blueprint \
  --output-dir ./agent_factory
```

This creates:
- `agent_factory/agents/research_assistant_config.yaml` - Agent configuration
- `agent_factory/tools/web_search.py` - Tool implementations
- `agent_factory/workflows/research_pipeline_workflow.yaml` - Workflow definition
- `blueprints/research_assistant/blueprint.yaml` - Blueprint package

## Step 3: Attach Knowledge Pack

Enhance your agent with domain-specific knowledge:

```bash
# List available knowledge packs
agent-factory knowledge-pack list

# Attach academic research pack
agent-factory knowledge-pack attach research-assistant academic-research
```

Knowledge packs provide:
- Pre-indexed domain knowledge
- RAG (Retrieval-Augmented Generation) capabilities
- Domain-specific context

## Step 4: Run Benchmarks

Evaluate your agent's performance:

```bash
# Run benchmark suite
agent-factory eval benchmark research-assistant --suite baseline

# Run stress test
agent-factory eval stress-test research-assistant --concurrent 10 --duration 60

# Auto-tune configuration
agent-factory eval autotune research-assistant --suite baseline --output tuned_config.yaml
```

Results help you:
- Measure accuracy and latency
- Identify bottlenecks
- Optimize configuration automatically

## Step 5: Generate UI / SaaS Scaffold

Create a user interface or full SaaS app:

```bash
# Generate UI
agent-factory ui generate research-assistant --output ui/research-assistant/ --template react

# Or create full SaaS scaffold
agent-factory saas create research-assistant --output ./apps/research-saas/
```

The UI generator creates:
- HTML/React frontend
- API endpoints
- Authentication stub
- Billing integration stub

The SaaS scaffold includes:
- FastAPI backend
- Frontend application
- Docker configuration
- Deployment docs

## Next Steps

- **Visualize workflows**: `agent-factory workflow visualize research-pipeline --format mermaid`
- **Review prompt logs**: `agent-factory promptlog list-runs --agent research-assistant`
- **Replay runs**: `agent-factory promptlog replay <run_id>`
- **Compare runs**: `agent-factory promptlog diff <run_id_1> <run_id_2>`

## Example: Complete Flow

```bash
# 1. Convert notebook
agent-factory notebook convert notebook.ipynb --agent-name my-agent

# 2. Attach knowledge pack
agent-factory knowledge-pack attach my-agent academic-research

# 3. Run benchmark
agent-factory eval benchmark my-agent --suite baseline

# 4. Auto-tune
agent-factory eval autotune my-agent --suite baseline

# 5. Generate UI
agent-factory ui generate my-agent --output ui/my-agent/

# 6. Deploy
cd ui/my-agent && docker-compose up
```

## Troubleshooting

**Conversion fails**: Ensure notebook follows conventions (see `docs/FEATURES.md`)

**Knowledge pack not found**: Install packs from registry or create your own

**Benchmark errors**: Check agent configuration and API keys

**UI generation fails**: Ensure agent has valid input/output schemas

## Learn More

- [Features Overview](FEATURES.md) - All platform features
- [Architecture](ARCHITECTURE_DETAILED.md) - System design
- [API Reference](API_REFERENCE.md) - REST API docs
