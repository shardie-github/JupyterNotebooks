# Agent Factory Platform

> Build production-ready AI agents for higher education in minutes, not months.

**Agent Factory** is a composable, extensible platform for building, deploying, and monetizing AI agents, strategically designed for **higher education institutions** and **lifelong learning organizations** in partnership with **McGraw Hill Education**.

Transform from notebooks to production with our Python library, CLI, and REST API. Perfect for creating virtual teaching assistants, personalized learning agents, research assistants, and more.

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

## 🎓 Education Focus

**Agent Factory Platform** is designed specifically for higher education institutions and lifelong learning organizations in strategic partnership with **McGraw Hill Education**.

### Education Use Cases

- **Virtual Teaching Assistants**: 24/7 student support and Q&A
- **Personalized Learning Paths**: Adaptive learning recommendations
- **Research Assistants**: Academic research and citation support
- **Assessment Tools**: Automated question generation and grading
- **Career Guidance**: Professional development and career planning
- **Content Curation**: Educational resource organization

### Partnership Information

- **Partnership Portal**: [www.mheducation.ca/partnerships](https://www.mheducation.ca/partnerships)
- **Lead Sources**: Partnership form and word of mouth referrals
- **Target Audience**: Universities, colleges, lifelong learning organizations

See [Education Focus Guide](/docs/EDUCATION_FOCUS.md) and [McGraw Hill Partnership](/docs/MHE_PARTNERSHIP.md) for more information.

## 📚 Documentation

- [Education Focus](/docs/EDUCATION_FOCUS.md) - Education-specific features and use cases
- [McGraw Hill Partnership](/docs/MHE_PARTNERSHIP.md) - Partnership details and benefits
- [Vision & Strategy](/docs/VISION_AND_STRATEGY.md)
- [Go-to-Market Plan](/docs/GTM_PLAN.md)
- [Pricing Tiers](/docs/PRICING_TIERS.md)
- [Use Case Blueprints](/docs/USE_CASE_BLUEPRINTS.md)
- [User Guide](/docs/USER_GUIDE.md)
- [Architecture Documentation](/docs/ARCHITECTURE_DETAILED.md)

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

## 📦 Education Blueprints

Install pre-built Blueprints designed for higher education:

```bash
# Install Student Support Assistant
agent-factory blueprint install student-support-assistant

# Install Learning Path Generator
agent-factory blueprint install learning-path-generator

# Install Assessment Assistant
agent-factory blueprint install assessment-assistant

# Search for Education Blueprints
agent-factory blueprint search "education"
```

### Available Education Blueprints

- **Student Support Assistant**: 24/7 virtual teaching assistant
- **Learning Path Generator**: Personalized adaptive learning paths
- **Research Assistant**: Academic research and citation support
- **Assessment Assistant**: Assessment creation and grading tools
- **Career Advisor**: Career guidance and professional development
- **Content Curator**: Educational resource curation

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

## 🤝 Partnership & Contact

### For Educational Institutions

Interested in partnering with Agent Factory Platform for your institution?

- **Partnership Portal**: [www.mheducation.ca/partnerships](https://www.mheducation.ca/partnerships)
- **Email**: partnerships@mheducation.ca
- **Referrals**: Word of mouth referrals welcome

### General Inquiries

- **Support**: support@agentfactory.io
- **Education Team**: education@agentfactory.io
- **Sales**: sales@agentfactory.io

## 🤝 Contributing

Contributions welcome! Please see our contributing guidelines.

## 📄 License

GPL-3.0 License - see [LICENSE](/LICENSE) file.

## 🔗 Links

- [Documentation](https://docs.agentfactory.io)
- [Marketplace](https://marketplace.agentfactory.io)
- [GitHub](https://github.com/agentfactory/platform)
- [McGraw Hill Education Partnerships](https://www.mheducation.ca/partnerships)

---

**Built with ❤️ by the Agent Factory Team**  
**In Strategic Partnership with McGraw Hill Education**
