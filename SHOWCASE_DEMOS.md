# Agent Factory - Showcase Demos

This document showcases various demos and examples of Agent Factory Platform in action.

## 🎮 Interactive Demo UI

### Launch the Demo

```bash
# Install demo dependencies
pip install 'agent-factory[demo]'

# Launch Streamlit demo
agent-factory ui demo
```

The demo UI includes:

1. **Agent Playground**: Test agents interactively
2. **Workflow Visualizer**: Visualize agent workflows with Mermaid diagrams
3. **Blueprint Browser**: Browse and explore available blueprints
4. **Prompt Log Viewer**: View execution logs and analytics

Access at: http://localhost:8501

## 📱 Example Applications

### Research Assistant App

A complete FastAPI application demonstrating Agent Factory integration.

**Location**: `apps/research_assistant_app/`

**Features**:
- AI-powered research queries
- Auto-generated web UI
- REST API with OpenAPI docs
- Docker deployment ready

**Run locally**:
```bash
cd apps/research_assistant_app
pip install -r requirements.txt
python main.py
```

**Deploy with Docker**:
```bash
docker build -t research-assistant .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key research-assistant
```

Access at: http://localhost:8000

## 🎯 Blueprint Examples

### 1. Research Assistant

**Install**:
```bash
agent-factory blueprint install research-assistant --marketplace
```

**Test**:
```bash
agent-factory blueprint test research-assistant --input "What is AI?"
```

**Features**:
- Web search integration
- Report generation
- Citation support

### 2. Student Support Assistant

**Install**:
```bash
agent-factory blueprint install student-support-assistant --marketplace
```

**Use Case**: 24/7 virtual teaching assistant for student questions

### 3. Learning Path Generator

**Install**:
```bash
agent-factory blueprint install learning-path-generator --marketplace
```

**Use Case**: Personalized adaptive learning paths

### 4. Assessment Assistant

**Install**:
```bash
agent-factory blueprint install assessment-assistant --marketplace
```

**Use Case**: Assessment creation and grading tools

## 💻 Code Examples

### Basic Agent

```python
from agent_factory import Agent

agent = Agent(
    id="greeting-agent",
    name="Greeting Agent",
    instructions="You are a friendly assistant.",
    tools=[]
)

result = agent.run("Hello!")
print(result.output)
```

### Agent with Tools

```python
from agent_factory import Agent
from agent_factory.integrations.tools.calculator import calculator

agent = Agent(
    id="calculator-agent",
    name="Calculator Agent",
    instructions="You are a calculator assistant.",
    tools=[calculator]
)

result = agent.run("What is 15 * 23?")
print(result.output)
```

### Multi-Agent Workflow

```python
from agent_factory import Agent, Workflow

# Create agents
researcher = Agent(id="researcher", name="Researcher", ...)
analyzer = Agent(id="analyzer", name="Analyzer", ...)

# Create workflow
workflow = Workflow(
    id="research-workflow",
    steps=[
        {"id": "research", "agent": "researcher"},
        {"id": "analyze", "agent": "analyzer", "depends_on": ["research"]}
    ]
)

# Run workflow
result = workflow.run("Research topic: AI in education")
```

## 🌐 Deployment Demos

### Docker Deployment

```bash
# Build
docker build -t agent-factory .

# Run
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  agent-factory
```

### Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

See `deployment/vercel.json` for configuration.

### Render Deployment

1. Connect GitHub repository
2. Render auto-detects `deployment/render.yaml`
3. Set environment variables
4. Deploy

### HuggingFace Spaces

1. Create new Space
2. Upload files from `deployment/huggingface/`
3. Set secrets (API keys)
4. Auto-deploys

## 📊 Demo Scenarios

### Scenario 1: Student Q&A Bot

**Goal**: Answer student questions 24/7

**Setup**:
```bash
agent-factory blueprint install student-support-assistant
agent-factory ui demo
```

**Usage**: Students ask questions, bot provides answers with citations

### Scenario 2: Research Paper Assistant

**Goal**: Help researchers find and analyze papers

**Setup**:
```bash
agent-factory blueprint install research-assistant
cd apps/research_assistant_app
python main.py
```

**Usage**: Researchers query topics, get comprehensive research summaries

### Scenario 3: Learning Path Generator

**Goal**: Create personalized learning paths

**Setup**:
```bash
agent-factory blueprint install learning-path-generator
agent-factory blueprint test learning-path-generator
```

**Usage**: Input learning goals, get customized curriculum

## 🎥 Video Demos

### Demo 1: Getting Started (5 min)
- Installation
- First agent
- Basic usage

### Demo 2: Building a Custom Agent (10 min)
- Creating tools
- Writing instructions
- Testing and debugging

### Demo 3: Blueprint System (8 min)
- Installing blueprints
- Creating custom blueprints
- Publishing to marketplace

### Demo 4: Deployment (12 min)
- Docker deployment
- Cloud platforms
- Production considerations

## 🚀 Live Demos

- **Demo Site**: https://demo.agentfactory.io
- **API Playground**: https://api.agentfactory.io/docs
- **Marketplace**: https://marketplace.agentfactory.io

## 📝 Demo Scripts

### Quick Demo Script

```bash
#!/bin/bash
# Quick demo script

echo "🚀 Agent Factory Quick Demo"
echo ""

# Check system
echo "1. Checking system..."
agent-factory doctor

# Show config
echo ""
echo "2. Current configuration..."
agent-factory config show

# List blueprints
echo ""
echo "3. Available blueprints..."
agent-factory blueprint list

# Test blueprint
echo ""
echo "4. Testing research assistant..."
agent-factory blueprint test research-assistant --input "What is AI?"

echo ""
echo "✅ Demo complete!"
```

## 🎓 Educational Demos

### For Instructors

- **Course Assistant**: Help with course planning and content
- **Grading Assistant**: Automated feedback generation
- **Content Curator**: Organize educational resources

### For Students

- **Study Buddy**: Answer questions and explain concepts
- **Writing Assistant**: Help with essays and reports
- **Career Advisor**: Career guidance and planning

## 🔗 Additional Resources

- **Examples Directory**: `/examples/` - More code examples
- **Documentation**: `/docs/` - Comprehensive guides
- **API Reference**: Auto-generated from code
- **Community**: GitHub Discussions

---

**Try the demos and see Agent Factory in action!** 🎉
