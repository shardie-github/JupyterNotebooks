# Agent Factory Platform - Features Overview

Complete guide to all platform features.

## Core Features

### 1. Notebook → Agent Converter

Automatically extract agents, tools, and workflows from Jupyter notebooks.

**Usage**:
```bash
agent-factory notebook convert notebook.ipynb --agent-name my-agent
```

**What it detects**:
- `Agent(...)` instantiations
- `@function_tool` decorated functions
- `Workflow(...)` definitions
- `AgentFactory.create_*()` patterns

**Output**:
- Agent configuration YAML files
- Tool Python implementations
- Workflow definitions
- Optional blueprint packages

### 2. Blueprints

Package agents, tools, workflows, and knowledge packs into reusable bundles.

**Usage**:
```bash
agent-factory blueprint create my-blueprint
agent-factory blueprint install research-assistant
agent-factory blueprint publish my-blueprint
```

**Features**:
- Dependency management
- Configuration templates
- Marketplace publishing
- Version control

### 3. Knowledge Packs

Pluggable RAG modules that enhance agents with domain-specific knowledge.

**Usage**:
```bash
agent-factory knowledge-pack attach my-agent academic-research
agent-factory knowledge-pack create finance-pack
```

**Features**:
- Vector store integration
- Multiple data sources
- Configurable embedding models
- Domain-specific retrievers

### 4. Workflow Visualization

Generate Mermaid/Graphviz diagrams from workflow definitions.

**Usage**:
```bash
agent-factory workflow visualize my-workflow --format mermaid --output workflow.md
```

**Formats**:
- Mermaid (for markdown/docs)
- Graphviz DOT (for PNG/SVG)

### 5. Prompt Logging, Replay & Diff

Log all agent runs, replay with different configs, and compare outputs.

**Usage**:
```bash
agent-factory promptlog list-runs --agent my-agent
agent-factory promptlog replay <run_id> --config override.yaml
agent-factory promptlog diff <run_id_1> <run_id_2>
```

**Features**:
- SQLite/JSONL storage
- Detailed prompt/response logs
- Config override replay
- Semantic and textual diff

### 6. Evaluation & AutoTune

Benchmark agents, stress test, and automatically optimize configurations.

**Usage**:
```bash
agent-factory eval benchmark my-agent --suite baseline
agent-factory eval stress-test my-agent --concurrent 10
agent-factory eval autotune my-agent --suite baseline
```

**Features**:
- Scenario-based evaluation
- Load testing
- Automatic config optimization
- Metrics tracking (accuracy, latency, cost)

### 7. Multi-Agent Orchestration

Coordinate multiple agents with routing and handoffs.

**Usage**:
```python
from agent_factory.orchestration import AgentGraph, OrchestrationExecutor

graph = AgentGraph(
    nodes=[...],
    edges=[...],
    entry_point="coordinator",
)

executor = OrchestrationExecutor()
result = executor.execute(graph, inputs={...})
```

**Features**:
- Agent graphs
- Conditional routing
- Message passing
- Handoff support

### 8. Zero-Config UI Generator

Generate web UIs for any agent based on its schema.

**Usage**:
```bash
agent-factory ui generate my-agent --output ui/my-agent/ --template react
```

**Features**:
- Schema inference from agent/tools
- HTML and React templates
- Input/output forms
- API integration

### 9. SaaS Starter Template

One-command generation of full SaaS apps from blueprints.

**Usage**:
```bash
agent-factory saas create research-assistant --output ./apps/research-saas/
```

**Includes**:
- FastAPI backend
- Frontend application
- Authentication stub
- Billing integration (Stripe)
- Docker configuration
- Deployment docs

## Integration Points

All features integrate with core primitives:

- **Agents**: Used by workflows, orchestration, eval, UI generator
- **Tools**: Used by agents, workflows, blueprints
- **Workflows**: Used by orchestration, visualizer, eval
- **Blueprints**: Package all components for reuse
- **Knowledge Packs**: Attach to agents/workflows
- **Prompt Log**: Wired through runtime engine
- **Eval**: Tests agents/workflows using same runtime

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Notebook Converter                    │
│              (Extracts agents/tools/workflows)           │
└────────────────────┬──────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Core Primitives (Engine)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  Agent   │  │   Tool   │  │ Workflow │            │
│  └──────────┘  └──────────┘  └──────────┘            │
└──────┬──────────────┬──────────────┬──────────────────┘
       │              │              │
       ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Blueprints   │ │  Knowledge  │ │ Orchestration│
│              │ │    Packs     │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
       │              │              │
       └──────────────┴──────────────┘
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Prompt Log │ │     Eval     │ │  UI Generator│
│              │ │   AutoTune    │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
       │              │              │
       └──────────────┴──────────────┘
                      │
                      ▼
              ┌──────────────┐
              │ SaaS Scaffold│
              └──────────────┘
```

## Feature Status

✅ **Implemented**:
- Notebook converter (basic)
- Blueprints (basic)
- Knowledge packs (model)
- Prompt logging (SQLite)
- Evaluation framework (basic)
- Workflow visualizer (Mermaid/Graphviz)
- Multi-agent orchestration (basic)
- UI generator (placeholder)
- SaaS scaffold (placeholder)

🚧 **In Progress**:
- Full notebook conversion (AST parsing improvements)
- Knowledge pack loaders (vector store integration)
- AutoTune (optimization algorithms)
- UI generator (React templates)

📋 **Planned**:
- Advanced orchestration (condition evaluation)
- Real-time collaboration
- Custom LLM providers
- Distributed execution

## Examples

See `examples/` directory for:
- `basic_agent.py` - Simple agent
- `multi_agent_system.py` - Multi-agent coordination
- `customer_support_bot.py` - Support bot template
- `education_learning_path.py` - Education use case
- `education_student_support.py` - Student support agent

## Documentation

- [Getting Started](GETTING_STARTED.md) - Quick start guide
- [Architecture](ARCHITECTURE_DETAILED.md) - System design
- [API Reference](API_REFERENCE.md) - REST API docs
- [User Guide](USER_GUIDE.md) - Detailed usage guide
