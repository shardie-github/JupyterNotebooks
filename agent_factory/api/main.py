"""
FastAPI REST API main application.
"""

import os
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from agent_factory.monitoring import setup_metrics, setup_structured_logging, setup_tracing
from agent_factory.security import setup_rate_limiting
from agent_factory.database import init_db
from agent_factory.cache import get_cache
from agent_factory.api.routes import agents, tools, workflows, blueprints, executions, telemetry

# Setup structured logging
logger = setup_structured_logging(os.getenv("LOG_LEVEL", "INFO"))

app = FastAPI(
    title="Agent Factory Platform API",
    description="REST API for building and running AI agents",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup monitoring
setup_metrics(app)
setup_tracing(app)

# Setup rate limiting
setup_rate_limiting(
    app,
    requests_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
    requests_per_hour=int(os.getenv("RATE_LIMIT_PER_HOUR", "1000"))
)


@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))


# Include routers
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(tools.router, prefix="/api/v1/tools", tags=["tools"])
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["workflows"])
app.include_router(blueprints.router, prefix="/api/v1/blueprints", tags=["blueprints"])
app.include_router(executions.router, prefix="/api/v1/executions", tags=["executions"])
app.include_router(telemetry.router, prefix="/api/v1/telemetry", tags=["telemetry"])

# Additional routers
from agent_factory.api.routes import scheduler, payments
app.include_router(scheduler.router, prefix="/api/v1/scheduler", tags=["scheduler"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["payments"])


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log all requests."""
    logger.info(
        "Request received",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host if request.client else "unknown"
    )
    
    response = await call_next(request)
    
    logger.info(
        "Request completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code
    )
    
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.exception(
        "Unhandled exception",
        error=str(exc),
        path=request.url.path,
        method=request.method
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": "Agent Factory Platform API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    health_status = {
        "status": "healthy",
        "database": "unknown",
        "cache": "unknown"
    }
    
    # Check database
    try:
        from agent_factory.database.session import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        health_status["database"] = "healthy"
    except Exception as e:
        health_status["database"] = "unhealthy"
        health_status["status"] = "degraded"
        logger.error("Database health check failed", error=str(e))
    
    # Check cache
    try:
        cache = get_cache()
        if cache.client:
            cache.client.ping()
            health_status["cache"] = "healthy"
        else:
            health_status["cache"] = "unavailable"
    except Exception as e:
        health_status["cache"] = "unhealthy"
        health_status["status"] = "degraded"
        logger.error("Cache health check failed", error=str(e))
    
    status_code = status.HTTP_200_OK if health_status["status"] == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(content=health_status, status_code=status_code)


@app.get("/ready")
async def readiness():
    """Readiness probe endpoint."""
    try:
        from agent_factory.database.session import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"status": "ready"}
    except Exception:
        return JSONResponse(
            content={"status": "not ready"},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@app.get("/live")
async def liveness():
    """Liveness probe endpoint."""
    return {"status": "alive"}
