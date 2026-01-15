# Contributing to Home Security Platform

We welcome contributions! This document outlines how to get started and guidelines for contributing.

## Development Environment

### Prerequisites

- Docker and Docker Compose
- Git
- Python 3.9+ (for local testing)
- Node.js (for web-ui development)

### Setup

1. Fork and clone the repository:
   ```
   git clone https://github.com/yourusername/home-security-platform.git
   cd home-security-platform
   ```

2. Start the services for development:
   ```
   docker-compose -f docker-compose.dev.yml up -d
   ```
   (Note: A development compose file mounts source code for hot reloading)

3. For individual service development:
   - Enter the service container: `docker-compose exec <service> bash`
   - Install dependencies and run locally if needed.

## Guidelines

### Code Principles

- **Local-First**: Ensure all features work without internet.
- **Reliability**: Use proven libraries; avoid experimental features.
- **Simplicity**: Prefer straightforward implementations over complex abstractions.
- **Security**: Validate inputs, use secure defaults.

### Pull Requests

- Create a feature branch: `git checkout -b feature/your-feature`
- Write clear commit messages.
- Include tests for new functionality.
- Update documentation if needed.
- Ensure CI passes (if set up).

### Code Style

- **Python**: Use Black for formatting, Flake8 for linting.
- **JavaScript/React**: Use ESLint and Prettier.
- **YAML/Docker**: Consistent indentation, comments for complex configs.

### Testing

- Add unit tests for services.
- Test integrations with other services.
- Manual testing: Verify in web UI.

## Architecture Contributions

- Propose changes in issues first.
- Maintain modularity; avoid tight coupling.
- Document inter-service changes.

## Security Considerations

- Review [Security Best Practices](../docs/security.md) before contributing.
- Avoid introducing security vulnerabilities.
- Use secure coding practices.
- Report security issues privately.

## Reporting Issues

- Use GitHub Issues.
- Include OS, Docker version, logs, and steps to reproduce.

## License

By contributing, you agree to license your work under the MIT License.