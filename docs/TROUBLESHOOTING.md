# Agent Factory Platform - Troubleshooting Guide

## Common Issues & Solutions

### API Server Won't Start

**Issue**: `uvicorn agent_factory.api.main:app` fails to start

**Solutions:**
1. Check Python version: `python --version` (requires 3.8+)
2. Verify dependencies: `pip install -e ".[dev]"`
3. Check port availability: `lsof -i :8000`
4. Review error logs for specific error messages

**Common Errors:**
- `ModuleNotFoundError`: Install missing dependencies
- `Address already in use`: Change port or stop existing process
- `Database connection failed`: Check DATABASE_URL

---

### Database Connection Issues

**Issue**: Cannot connect to database

**Solutions:**
1. Verify DATABASE_URL format:
   ```
   postgresql://user:password@host:5432/dbname
   ```
2. Check database is running:
   ```bash
   # PostgreSQL
   pg_isready -h localhost -p 5432
   ```
3. Verify credentials and permissions
4. Check firewall/network connectivity

**SQLite (Development):**
- Ensure directory is writable
- Check file permissions
- Verify path is correct

---

### LLM API Errors

**Issue**: OpenAI/Anthropic API calls failing

**Solutions:**
1. Verify API key is set:
   ```bash
   echo $OPENAI_API_KEY
   ```
2. Check API key is valid and has credits
3. Verify network connectivity
4. Check rate limits (429 errors)
5. Review API error messages

**Common Errors:**
- `401 Unauthorized`: Invalid API key
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: API provider issue

---

### Import Errors

**Issue**: `ImportError` or `ModuleNotFoundError`

**Solutions:**
1. Activate virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Reinstall package:
   ```bash
   pip install -e "."
   ```
3. Check Python path
4. Verify package is installed: `pip list | grep agent-factory`

---

### Rate Limiting Issues

**Issue**: Getting 429 Too Many Requests

**Solutions:**
1. Check rate limit configuration:
   ```bash
   RATE_LIMIT_PER_MINUTE=60
   RATE_LIMIT_PER_HOUR=1000
   ```
2. Review rate limit headers in response
3. Implement exponential backoff in client
4. Consider increasing limits if legitimate

---

### Health Check Failing

**Issue**: `/health` endpoint returns degraded status

**Solutions:**
1. Check database connectivity
2. Verify Redis/cache is accessible
3. Review health check logs
4. Check individual component status:
   ```bash
   curl http://localhost:8000/health | jq
   ```

---

### Agent Execution Errors

**Issue**: Agent runs fail or timeout

**Solutions:**
1. Check agent configuration (model, temperature)
2. Verify tools are properly registered
3. Review agent execution logs
4. Check LLM API status
5. Verify input is valid

**Common Errors:**
- `AgentExecutionError`: Check LLM API and configuration
- `TimeoutError`: Increase timeout or simplify agent
- `ToolExecutionError`: Check tool implementation

---

### Workflow Execution Errors

**Issue**: Workflows fail or don't complete

**Solutions:**
1. Verify all agents in workflow are registered
2. Check step conditions are valid
3. Review input/output mappings
4. Check workflow execution logs
5. Verify dependencies between steps

---

### File I/O Errors

**Issue**: File read/write operations fail

**Solutions:**
1. Check file path is within allowed directory
2. Verify file permissions
3. Check sandbox directory configuration:
   ```bash
   export AGENT_FACTORY_SANDBOX_DIR=/path/to/sandbox
   ```
4. Review path validation errors

**Common Errors:**
- `ToolValidationError`: Path traversal detected
- `PermissionError`: Insufficient file permissions
- `FileNotFoundError`: File doesn't exist

---

### Memory/Session Issues

**Issue**: Agent memory not persisting

**Solutions:**
1. Verify session_id is being passed
2. Check memory store is initialized
3. Verify database is accessible
4. Check memory store configuration

---

### Performance Issues

**Issue**: Slow API responses or agent execution

**Solutions:**
1. Enable Redis caching:
   ```bash
   REDIS_URL=redis://localhost:6379/0
   ```
2. Check database query performance
3. Review agent configuration (model, max_tokens)
4. Monitor system resources
5. Check for N+1 query patterns

---

### Debug Mode

**Enable debug mode for detailed errors:**

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
```

**Warning**: Never enable in production!

---

## Getting Help

### Check Logs

```bash
# API logs
tail -f logs/api.log

# Application logs (if logging to file)
# Check stdout/stderr for structured JSON logs
```

### Health Endpoints

```bash
# Overall health
curl http://localhost:8000/health

# Readiness
curl http://localhost:8000/ready

# Liveness
curl http://localhost:8000/live
```

### Common Commands

```bash
# Check environment
env | grep AGENT_FACTORY

# Test database connection
python -c "from agent_factory.database import init_db; init_db()"

# Test Redis connection
python -c "from agent_factory.cache import get_cache; cache = get_cache(); cache.client.ping()"

# Run tests
pytest tests/ -v

# Check code quality
ruff check agent_factory/
black --check agent_factory/
mypy agent_factory/
```

---

## Still Stuck?

1. **Check Documentation**: Review relevant docs in `docs/`
2. **Search Issues**: Check GitHub issues for similar problems
3. **Open Issue**: Create detailed issue with:
   - Error messages
   - Steps to reproduce
   - Environment details
   - Logs (sanitized)
4. **Community**: Ask in discussions/forums

---

**Last Updated**: 2024-01-XX  
**Version**: 0.1.0
