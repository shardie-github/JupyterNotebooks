# Agent Factory Platform

> Build production-ready AI agents in minutes, not months.

**Agent Factory** is a composable, extensible platform for building, deploying, and monetizing AI agents. Transform from notebooks to production with our Python library, CLI, and REST API.

## 🚀 Quick Start

### Installation

```bash
pip install agent-factory
```

### Create Your First Agent

```python
from agent_factory import Agent, function_tool

@function_tool
def calculate(expression: str) -> float:
    """Calculate mathematical expressions."""
    return eval(expression)

agent = Agent(
    id="my-agent",
    name="My Agent",
    instructions="You are a helpful assistant.",
    tools=[calculate],
)

result = agent.run("Calculate 15% tip on $87.50")
print(result.output)
```

### Using the CLI

```bash
# Initialize a project
agent-factory init my_project

# Create an agent
agent-factory agent create my-agent --name "My Agent" --instructions "You are helpful"

# Run an agent
agent-factory agent run my-agent --input "Hello!"
```

### Using the API

```bash
# Start the API server
uvicorn agent_factory.api.main:app --reload

# Create an agent via API
curl -X POST http://localhost:8000/api/v1/agents/ \
  -H "Content-Type: application/json" \
  -d '{"id": "my-agent", "name": "My Agent", "instructions": "You are helpful"}'
```

## 📚 Documentation

- [Vision & Strategy](/docs/VISION_AND_STRATEGY.md)
- [Go-to-Market Plan](/docs/GTM_PLAN.md)
- [Pricing Tiers](/docs/PRICING_TIERS.md)
- [Use Case Blueprints](/docs/USE_CASE_BLUEPRINTS.md)

## 🏗️ Architecture

```
agent_factory/
├── core/           # Core primitives (Agent, Tool, Workflow, Blueprint)
├── registry/       # Local and remote registries
├── runtime/        # Execution engine
├── integrations/   # Pre-built integrations (OpenAI, Anthropic, etc.)
├── api/            # FastAPI REST API
└── cli/            # Typer CLI interface
```

## 🎯 Key Features

- **Composable Agents**: Mix and match agents, tools, and workflows
- **Production Ready**: Built-in memory, guardrails, and observability
- **Blueprint System**: Install pre-configured agent bundles
- **Marketplace**: Discover and monetize agent components
- **CLI & API**: Use via command line or REST API

## 📦 Blueprints

Install pre-built Blueprints for common use cases:

```bash
# Install Support Bot Blueprint
agent-factory blueprint install support-bot-pro

# Search for Blueprints
agent-factory blueprint search "customer support"
```

## 🔧 Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black agent_factory/

# Type check
mypy agent_factory/
```

## 📝 Examples

See the [examples/](/examples/) directory for:
- Basic agent usage
- Multi-agent systems
- Customer support bot
- Research assistant

## 🤝 Contributing

Contributions welcome! Please see our contributing guidelines.

## 📄 License

GPL-3.0 License - see [LICENSE](/LICENSE) file.

## 🔗 Links

- [Documentation](https://docs.agentfactory.io)
- [Marketplace](https://marketplace.agentfactory.io)
- [GitHub](https://github.com/agentfactory/platform)

---

**Built with ❤️ by the Agent Factory Team**
