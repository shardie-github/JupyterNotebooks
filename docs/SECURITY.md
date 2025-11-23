# Agent Factory Platform - Security Guide

## Overview

This document outlines security best practices, features, and guidelines for the Agent Factory Platform.

---

## Security Features

### Input Validation

**All inputs are validated** using Pydantic models and custom validators:

- API endpoints validate request bodies
- Tool parameters are validated before execution
- File paths are sanitized and validated
- Expression evaluation uses safe AST-based evaluator (no eval())

### Authentication & Authorization

- **JWT Authentication**: Token-based authentication for API access
- **API Keys**: Programmatic access via API keys
- **RBAC**: Role-based access control for fine-grained permissions

### Rate Limiting

- **Per-IP Rate Limiting**: Configurable limits per minute/hour
- **Rate Limit Headers**: X-RateLimit-* headers in responses
- **429 Responses**: Proper HTTP 429 status codes

### Security Headers

All responses include security headers:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`
- `Content-Security-Policy: default-src 'self'`
- `Referrer-Policy: strict-origin-when-cross-origin`

### Safe Evaluation

- **No eval() usage**: All expression evaluation uses AST-based safe evaluator
- **Path Validation**: File operations validate paths to prevent traversal
- **SQL Injection Protection**: Guardrails detect SQL injection patterns

---

## Security Best Practices

### Secrets Management

**Never commit secrets to git:**

```bash
# ✅ Good: Use environment variables
export OPENAI_API_KEY=sk-...

# ❌ Bad: Hardcode in code
api_key = "sk-..."  # NEVER DO THIS
```

**Use secret management services in production:**
- Kubernetes Secrets
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault

### Environment Variables

**Required for production:**
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (at least one)
- `JWT_SECRET_KEY` (use strong random key)
- `DATABASE_URL` (use encrypted connection)

**Security-sensitive:**
- `JWT_SECRET_KEY`: Use cryptographically secure random key (min 32 chars)
- `API_KEY_SECRET`: For API key signing
- `STRIPE_SECRET_KEY`: For payment processing

### API Security

**Use HTTPS in production:**
- Never expose API over HTTP in production
- Use TLS 1.2+ with strong ciphers
- Configure proper certificate management

**Rate Limiting:**
- Configure appropriate limits per endpoint
- Monitor for abuse
- Implement IP-based blocking if needed

### Database Security

**Connection Security:**
- Use encrypted connections (SSL/TLS)
- Use strong passwords
- Limit database access to application servers only

**Query Security:**
- Use parameterized queries (SQLAlchemy does this)
- Never use string concatenation for SQL
- Validate all inputs before database operations

### File Operations

**Path Validation:**
- All file paths are validated
- Path traversal attacks are prevented
- Sandbox directory can be configured via `AGENT_FACTORY_SANDBOX_DIR`

**Example:**
```python
# ✅ Safe: Uses validated path
read_file("data/file.txt")  # Validated and sanitized

# ❌ Blocked: Path traversal attempt
read_file("../../../etc/passwd")  # Rejected
```

---

## Security Checklist

### Development

- [ ] Never commit secrets to git
- [ ] Use environment variables for all secrets
- [ ] Enable debug mode only in development
- [ ] Review code for security issues
- [ ] Run security linters

### Production

- [ ] Use HTTPS/TLS
- [ ] Set strong JWT_SECRET_KEY
- [ ] Configure rate limiting
- [ ] Enable security headers
- [ ] Use encrypted database connections
- [ ] Set up monitoring and alerting
- [ ] Regular security updates
- [ ] Backup and recovery plan
- [ ] Access control and RBAC
- [ ] Audit logging enabled

---

## Common Vulnerabilities & Mitigations

### SQL Injection

**Mitigation:**
- SQLAlchemy uses parameterized queries
- Never use string formatting for SQL
- Input validation before database operations

### Path Traversal

**Mitigation:**
- Path validation in file I/O tools
- Sandbox directory configuration
- Relative path resolution

### Code Injection

**Mitigation:**
- No eval() usage
- Safe AST-based evaluator
- Input sanitization

### XSS (Cross-Site Scripting)

**Mitigation:**
- Content Security Policy headers
- Input validation and sanitization
- Output encoding

### CSRF (Cross-Site Request Forgery)

**Mitigation:**
- Use authentication tokens
- Verify origin headers
- SameSite cookie attributes

---

## Security Monitoring

### Logging

- All security events are logged
- Failed authentication attempts
- Rate limit violations
- Suspicious patterns

### Alerting

Set up alerts for:
- Multiple failed authentication attempts
- Rate limit violations
- Unusual access patterns
- Error spikes

---

## Reporting Security Issues

**If you discover a security vulnerability:**

1. **Do NOT** open a public issue
2. Email: security@agentfactory.io
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

**We will:**
- Acknowledge receipt within 48 hours
- Investigate and respond within 7 days
- Fix and release patch as soon as possible
- Credit you in security advisories (if desired)

---

## Security Updates

- **Regular Updates**: Keep dependencies updated
- **Security Patches**: Apply promptly
- **Vulnerability Scanning**: Regular scans recommended
- **Dependency Audits**: Use tools like `safety` or `pip-audit`

---

## Compliance

### GDPR

- Data minimization
- Right to deletion
- Data portability
- Privacy by design

### SOC 2

- Access controls
- Encryption
- Monitoring
- Incident response

---

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security.html)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

---

**Last Updated**: 2024-01-XX  
**Version**: 0.1.0
