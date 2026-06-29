# Contributing to FDIA

First off, thanks for taking the time to contribute! ❤️

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

- Follow the Python style guide (Black, isort, ruff)
- Include appropriate test cases
- Update documentation as needed
- Add an entry to the CHANGELOG
- End all files with a newline
- Use conventional commit messages

## Development Setup

```bash
# Clone and setup
git clone https://github.com/deeptripathi8154-arch/fdia.git
cd fdia

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
make install-dev

# Enable pre-commit hooks
pre-commit install
```

## Conventional Commits

Use conventional commit messages:

```
feat: add new feature
fix: fix a bug
docs: documentation changes
style: code style changes (black, isort)
refactor: code refactoring
perf: performance improvements
test: test additions/updates
chore: build, dependencies, tooling
```

## Style Guide

### Python Style

- Follow PEP 8
- Use type hints for all functions
- Line length: 100 characters
- Docstring format: Google style

```python
def process_document(doc_path: str) -> dict[str, Any]:
    """Process a finance document and extract fields.
    
    Args:
        doc_path: Path to the document file
        
    Returns:
        Dictionary containing extracted fields
        
    Raises:
        FileNotFoundError: If document not found
        ValueError: If document is invalid
    """
```

### Code Organization

```
packages/
  your_package/
    __init__.py
    models.py           # Domain models
    repositories.py     # Data access
    services.py         # Business logic
    schemas.py          # Request/response schemas
    exceptions.py       # Custom exceptions
    constants.py        # Constants
    utils.py            # Utilities
```

## Testing

All new code must include tests.

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=packages --cov=apps

# Run specific test
pytest tests/unit/test_validators.py::test_imei_validation
```

### Test Structure

```
tests/
  unit/                 # Unit tests
  integration/          # Integration tests
  e2e/                  # End-to-end tests
  fixtures/             # Test fixtures
  conftest.py           # Pytest configuration
```

### Example Test

```python
import pytest
from packages.validation import ImeiValidator


class TestImeiValidator:
    """Test IMEI validation logic."""
    
    def test_valid_imei(self):
        """Test validation of valid IMEI."""
        assert ImeiValidator.validate("355283062232144")
    
    def test_invalid_imei(self):
        """Test rejection of invalid IMEI."""
        assert not ImeiValidator.validate("123456789")
    
    @pytest.mark.parametrize("imei", [
        "355283062232144",
        "359528506821234",
    ])
    def test_valid_imeis(self, imei):
        """Test multiple valid IMEIs."""
        assert ImeiValidator.validate(imei)
```

## Commit Process

```bash
# Format and lint
make format
make lint

# Run tests
make test

# Commit
git commit -m "feat: add IMEI validation"

# Push to feature branch
git push origin feature/your-feature

# Create pull request
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions
- Update docs/ for architecture/design changes
- Add migration documentation for DB changes

## Questions?

- Create a GitHub Discussion
- Ask in a GitHub Issue
- Email maintainers

Thank you for contributing! 🎉
