# Agent Factory

**Build production-ready AI agents in minutes, not months.**

Agent Factory is a platform that helps you turn AI prototypes into real products. Whether you're building a customer support bot, a research assistant, or an educational tool, we give you everything you need to go from idea to deployment—without the usual headaches.

## Why Agent Factory?

Building AI agents shouldn't require a team of engineers and months of work. We've seen too many great ideas die in Jupyter notebooks because the jump to production felt impossible.

Agent Factory fixes that. We've built the infrastructure, handled the complexity, and created a simple way to compose agents, tools, and workflows. You focus on what makes your agent unique. We handle the rest.

## What You Get

**Composable Building Blocks**
- Create agents with natural language instructions
- Add tools and capabilities as you need them
- Chain agents together into workflows
- Everything works together seamlessly

**Production Ready, Out of the Box**
- Built-in memory and conversation context
- Error handling and retries
- Observability and logging
- Rate limiting and security

**Blueprint System**
- Install pre-built agent configurations
- Share your own creations
- Build on what others have made
- Skip the setup, start building

**Multiple Ways to Use**
- Python library for developers
- CLI for quick prototyping
- REST API for integrations
- SDK for programmatic access

## Real-World Use Cases

**Customer Support**
Build bots that actually help customers. Handle common questions, escalate when needed, and learn from every interaction.

**Research Assistants**
Create agents that help researchers find papers, summarize findings, and organize information. Perfect for academic teams and knowledge workers.

**Educational Tools**
Build personalized learning assistants that adapt to each student. Generate practice questions, explain concepts, and track progress.

**Internal Automation**
Automate repetitive workflows. Process documents, route requests, generate reports—all with agents that understand context.

**SaaS Products**
Turn your agent into a product. We handle billing, multi-tenancy, and scaling so you can focus on your users.

## Quick Start

### Installation

```bash
pip install agent-factory
```

### Your First Agent

```python
from agent_factory import Agent, function_tool

@function_tool
def calculate(expression: str) -> float:
    """Calculate mathematical expressions."""
    return eval(expression)

agent = Agent(
    id="calculator",
    name="Calculator Agent",
    instructions="You are a helpful calculator assistant.",
    tools=[calculate],
)

result = agent.run("What's 15% tip on $87.50?")
print(result.output)
```

### Using the CLI

```bash
# Create an agent
agent-factory agent create calculator \
  --name "Calculator Agent" \
  --instructions "You help with math"

# Run it
agent-factory agent run calculator --input "Calculate 20% of 100"
```

### Using the API

```bash
# Start the server
uvicorn agent_factory.api.main:app --reload

# Create an agent
curl -X POST http://localhost:8000/api/v1/agents/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "calculator",
    "name": "Calculator Agent",
    "instructions": "You help with math"
  }'
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Your Application                      │
├─────────────────────────────────────────────────────────┤
│  Python SDK  │  CLI  │  REST API  │  Blueprints        │
├─────────────────────────────────────────────────────────┤
│              Agent Factory Platform                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Agents  │  │  Tools   │  │Workflows │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Registry │  │ Runtime  │  │Telemetry │             │
│  └──────────┘  └──────────┘  └──────────┘             │
├─────────────────────────────────────────────────────────┤
│  OpenAI  │  Anthropic  │  Custom Integrations         │
└─────────────────────────────────────────────────────────┘
```

## Project Structure

```
agent_factory/
├── core/              # Core primitives (Agent, Tool, Workflow)
├── agents/            # Agent implementations
├── tools/             # Tool system
├── workflows/         # Workflow orchestration
├── blueprints/        # Blueprint system
├── registry/          # Local and remote registries
├── runtime/           # Execution engine
├── api/               # REST API
├── cli/               # Command-line interface
├── sdk/               # Python SDK
├── telemetry/         # Analytics and metrics
├── security/          # Auth, RBAC, audit logging
├── billing/           # Usage tracking and billing
└── integrations/      # LLM providers and tools
```

## Key Features

**Memory & Context**
Agents remember conversations and maintain context across sessions. Perfect for support bots and personal assistants.

**Tool System**
Give agents superpowers. Add web search, file operations, API calls, or custom functions. Tools are composable and reusable.

**Workflow Orchestration**
Chain agents together. Build complex multi-step processes where each agent handles a specific task.

**Blueprint Marketplace**
Discover pre-built agent configurations. Install student support assistants, research tools, or customer service bots in seconds.

**Observability**
See what your agents are doing. Track usage, monitor performance, debug issues, and understand costs.

**Security & Compliance**
Built-in authentication, role-based access control, audit logging, and data retention policies. Ready for enterprise use.

## Education Focus

Agent Factory is designed with education in mind. We partner with institutions to build tools that help students learn and teachers teach.

**Education Use Cases**
- Virtual teaching assistants available 24/7
- Personalized learning paths that adapt to each student
- Research assistants that help with citations and papers
- Assessment tools that generate and grade questions
- Career guidance and professional development

**Partnership**
We work with McGraw Hill Education and other partners to bring AI tools to educational institutions. Learn more at [mheducation.ca/partnerships](https://www.mheducation.ca/partnerships).

## Examples

Check out the [examples/](examples/) directory for:
- Basic agent usage
- Multi-agent systems
- Customer support bots
- Research assistants
- Educational tools

## Documentation

- [Getting Started Guide](docs/GETTING_STARTED.md) - Detailed setup and first steps
- [User Guide](docs/USER_GUIDE.md) - Complete feature documentation
- [Architecture](docs/ARCHITECTURE_DETAILED.md) - Deep dive into how it works
- [API Reference](docs/API_REFERENCE.md) - REST API documentation
- [Use Cases](docs/USE_CASE_BLUEPRINTS.md) - Real-world examples

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linters
ruff check agent_factory/ tests/
black --check agent_factory/ tests/

# Type checking
mypy agent_factory/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

## CI/CD

Our CI pipeline runs on every commit:
- Linting and code formatting checks
- Type checking with mypy
- Unit and integration tests
- Docker image builds

Tests are designed to run without external services, making CI fast and reliable.

## Community

**Getting Help**
- Open an issue on GitHub for bugs or feature requests
- Check existing issues and discussions
- Read the documentation

**Contributing**
We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Partnerships**
Interested in partnering? Reach out at partnerships@agentfactory.io

## License

GPL-3.0 License - see [LICENSE](LICENSE) file.

## Links

- [Documentation](https://docs.agentfactory.io)
- [Marketplace](https://marketplace.agentfactory.io)
- [GitHub](https://github.com/agentfactory/platform)
- [McGraw Hill Education Partnerships](https://www.mheducation.ca/partnerships)

---

**Built by developers, for developers.**  
**Making AI agents accessible to everyone.**
