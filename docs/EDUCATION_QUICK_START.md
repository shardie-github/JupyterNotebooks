# Education Quick Start Guide

## For Higher Education Institutions

Welcome to Agent Factory Platform! This guide will help you get started quickly with creating AI agents for your educational institution.

## Partnership Setup

### Step 1: Contact McGraw Hill Education

1. Visit [www.mheducation.ca/partnerships](https://www.mheducation.ca/partnerships)
2. Complete the partnership inquiry form
3. Or reach out via word of mouth referral

### Step 2: Initial Consultation

- Discuss your institution's needs
- Identify specific use cases
- Plan pilot program
- Set up technical requirements

### Step 3: Account Setup

- Create institutional tenant
- Configure SSO (if applicable)
- Set up LMS integration
- Deploy initial agents

## Quick Start: Student Support Assistant

### Install Agent Factory

```bash
pip install agent-factory
```

### Create Your First Education Agent

```python
from agent_factory.core.agent import Agent

# Create student support agent
agent = Agent(
    id="student-support",
    name="Student Support Assistant",
    instructions="""
    You are a helpful virtual teaching assistant.
    Answer student questions about course content, assignments, and deadlines.
    Be supportive, clear, and encouraging.
    """,
    model="gpt-4o"
)

# Run the agent
result = agent.run("What is the deadline for Assignment 3?")
print(result.output)
```

### Using Pre-Built Education Blueprints

```bash
# Install Student Support Assistant blueprint
agent-factory blueprint install student-support-assistant

# Install Learning Path Generator
agent-factory blueprint install learning-path-generator

# Install Assessment Assistant
agent-factory blueprint install assessment-assistant
```

## Common Education Use Cases

### 1. Virtual Teaching Assistant

**Use Case**: 24/7 student support
**Blueprint**: `student-support-assistant`

```python
from agent_factory.core.agent import Agent

agent = Agent(
    id="virtual-ta",
    name="Virtual TA",
    instructions="Answer student questions about the course.",
    model="gpt-4o"
)

# Handle student questions
response = agent.run(student_question, session_id=student_id)
```

### 2. Personalized Learning Paths

**Use Case**: Adaptive learning recommendations
**Blueprint**: `learning-path-generator`

```python
agent = Agent(
    id="learning-path",
    name="Learning Path Generator",
    instructions="Create personalized learning paths for students.",
    model="gpt-4o"
)

path = agent.run(f"Create learning path for: {student_profile}")
```

### 3. Assessment Generation

**Use Case**: Create assessments and rubrics
**Blueprint**: `assessment-assistant`

```python
agent = Agent(
    id="assessment",
    name="Assessment Assistant",
    instructions="Generate assessment questions and rubrics.",
    model="gpt-4o"
)

assessment = agent.run(f"Create assessment for: {learning_objectives}")
```

## Integration with LMS

### Canvas Integration

```python
from agent_factory.integrations.lms.canvas import CanvasIntegration

canvas = CanvasIntegration(
    api_key="your-canvas-api-key",
    base_url="https://your-school.instructure.com"
)

# Sync student roster
students = canvas.get_students(course_id="12345")

# Create agent for course
agent = Agent(
    id=f"course-{course_id}-assistant",
    name=f"Course {course_id} Assistant",
    instructions="Help students with this course.",
    model="gpt-4o"
)
```

### Blackboard Integration

```python
from agent_factory.integrations.lms.blackboard import BlackboardIntegration

bb = BlackboardIntegration(
    api_key="your-blackboard-api-key",
    base_url="https://your-school.blackboard.com"
)
```

## Best Practices for Education

### 1. Student Privacy (FERPA Compliance)

- Always use session IDs for student interactions
- Don't store personally identifiable information
- Enable audit logging
- Use secure authentication

### 2. Accessibility

- Ensure agents provide clear, structured responses
- Support screen readers
- Use accessible formats
- Test with accessibility tools

### 3. Faculty Training

- Provide comprehensive training materials
- Offer hands-on workshops
- Create faculty-specific documentation
- Establish support channels

### 4. Student Onboarding

- Create student orientation materials
- Provide clear usage instructions
- Set expectations appropriately
- Gather feedback regularly

## Support & Resources

### Documentation

- [Education Focus Guide](/docs/EDUCATION_FOCUS.md)
- [McGraw Hill Partnership](/docs/MHE_PARTNERSHIP.md)
- [User Guide](/docs/USER_GUIDE.md)
- [Examples Gallery](/docs/EXAMPLES_GALLERY.md)

### Support Channels

- **Education Support**: education@agentfactory.io
- **Partnership Inquiries**: partnerships@mheducation.ca
- **Technical Support**: support@agentfactory.io

### Training Resources

- Video tutorials
- Webinar series
- Faculty workshops
- Community forum

## Next Steps

1. **Explore Blueprints**: Browse available education blueprints
2. **Create Pilot**: Start with a small pilot program
3. **Gather Feedback**: Collect student and faculty feedback
4. **Scale Up**: Expand to additional courses/programs
5. **Optimize**: Refine based on usage and feedback

## Success Metrics

Track these metrics to measure success:

- **Student Engagement**: Response rate, usage frequency
- **Response Quality**: Student satisfaction ratings
- **Faculty Adoption**: Number of faculty using agents
- **Time Savings**: Reduction in support workload
- **Learning Outcomes**: Improved student performance

---

**Ready to get started?**  
Contact [McGraw Hill Education Partnerships](https://www.mheducation.ca/partnerships) today!
