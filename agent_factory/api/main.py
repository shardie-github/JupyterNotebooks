"""
FastAPI REST API main application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent_factory.api.routes import agents, tools, workflows, blueprints, executions

app = FastAPI(
    title="Agent Factory Platform API",
    description="REST API for building and running AI agents",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(tools.router, prefix="/api/v1/tools", tags=["tools"])
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["workflows"])
app.include_router(blueprints.router, prefix="/api/v1/blueprints", tags=["blueprints"])
app.include_router(executions.router, prefix="/api/v1/executions", tags=["executions"])


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": "Agent Factory Platform API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}
