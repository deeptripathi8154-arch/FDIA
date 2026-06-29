# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | ✅ Development     |

## Reporting a Vulnerability

**Do NOT create a public GitHub issue for security vulnerabilities.**

Please email security@fdia.local with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You should receive a response within 48 hours.

## Security Best Practices

### Environment Variables
- Never commit `.env` files
- Use `.env.example` as a template
- Rotate secrets regularly
- Use strong, unique passwords

### Database
- Always use parameterized queries (SQLAlchemy does this)
- Enable SSL for database connections in production
- Use strong database passwords
- Restrict database access to application servers

### API
- Enable CORS only for trusted domains
- Validate and sanitize all inputs
- Use rate limiting
- Implement request size limits
- Use HTTPS in production

### Authentication
- Hash passwords with bcrypt
- Use JWT with expiration
- Implement logout functionality
- Use secure session management

### Dependencies
- Keep dependencies updated
- Review dependency changes in PRs
- Use security scanning tools
- Pin versions in requirements.txt

### Code
- Use type hints to catch errors
- Run security linters (bandit)
- Validate external inputs
- Use SAST tools
- Conduct regular security reviews

## Compliance

This project aims to comply with:
- OWASP Top 10
- CWE Top 25
- GDPR (for data handling)
- PCI DSS (for payment data, if applicable)
