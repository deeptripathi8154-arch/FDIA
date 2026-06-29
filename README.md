# Finance Document Intelligence Agent (FDIA)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎯 Overview

**FDIA** is an enterprise-grade Finance Document Intelligence Agent built as a monorepo for automating document processing, OCR extraction, AI-powered field normalization, and Excel export workflows. The system is designed to evolve from a desktop application into a complete finance automation platform with cloud synchronization capabilities.

### Core Capabilities

- 🤖 **Desktop Automation** - WhatsApp/Web automation using Playwright
- 📸 **OCR Processing** - Multi-engine OCR (PaddleOCR, EasyOCR)
- 🧠 **AI Extraction** - Ollama-powered field normalization
- 💾 **Database Management** - SQLAlchemy + Alembic migrations
- 📊 **Excel Export** - Automated workbook generation
- ⚡ **Background Worker** - APScheduler-based task processing
- 🔌 **FastAPI** - REST endpoints for search and reporting
- 🖥️ **Flet Desktop** - Cross-platform dashboard

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Docker & Docker Compose (optional)
- Git

### Local Development

```bash
# Clone repository
git clone https://github.com/deeptripathi8154-arch/fdia.git
cd fdia

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install-dev

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start PostgreSQL and Redis
make docker-up

# Run migrations
make migrate

# Start the worker
make run-worker

# In another terminal, start the API
make run-api

# In another terminal, start the desktop app
make run-desktop
```

## 🏗️ Architecture

### Monorepo Layout

```
fdia/
├── apps/                          # Runnable applications
│   ├── api/                       # FastAPI service
│   ├── worker/                    # Background processing
│   ├── desktop/                   # Flet desktop UI
│   └── installer/                 # Windows packaging
│
├── packages/                      # Reusable packages
│   ├── automation/                # Playwright automation
│   ├── ocr/                       # OCR engines
│   ├── ai/                        # AI extraction
│   ├── parser/                    # PDF parsing
│   ├── excel/                     # Excel export
│   ├── database/                  # SQLAlchemy models
│   ├── models/                    # Domain models
│   ├── repositories/              # Data access layer
│   ├── services/                  # Business logic
│   ├── validation/                # Validators
│   ├── notifications/             # Alerts
│   ├── logging/                   # Loguru config
│   ├── config/                    # Settings
│   ├── security/                  # Auth & encryption
│   ├── monitoring/                # Health checks
│   ├── scheduler/                 # Job scheduling
│   ├── storage/                   # File management
│   └── shared/                    # Utilities
│
├── docs/                          # Documentation
├── infrastructure/                # DevOps configs
├── tests/                         # Test suite
├── data/                          # Data storage
└── logs/                          # Application logs
```

### Design Principles

- **Clean Architecture** - Clear separation of concerns
- **Domain-Driven Design** - Models reflect business domains
- **Repository Pattern** - Abstracted data access
- **Dependency Injection** - Loose coupling
- **SOLID Principles** - Maintainable, scalable code
- **Type Safety** - Python type hints throughout
- **Async-first** - Performance where it matters
- **Test-driven** - Comprehensive test coverage

## 📦 Project Structure

### Apps

#### API (`apps/api/`)
FastAPI REST service for searching records and generating reports. Provides dashboard data, health monitoring, and future mobile integration endpoints.

#### Worker (`apps/worker/`)
Background processing service that monitors WhatsApp, downloads files, performs OCR, extracts fields via AI, updates database, and generates Excel exports.

#### Desktop (`apps/desktop/`)
Flet-based cross-platform dashboard for configuration, monitoring, and search.

#### Installer (`apps/installer/`)
Windows executable packaging resources.

### Core Packages

#### `packages/database/`
- SQLAlchemy ORM models
- Alembic migrations
- Connection pooling
- Repository implementations

#### `packages/models/`
- Domain entities
- Value objects
- Domain events

#### `packages/services/`
- Business logic
- Transactional boundaries
- Orchestration

#### `packages/repositories/`
- Data access abstraction
- Query interfaces

#### `packages/automation/`
- Playwright session management
- Attachment detection
- File downloading

#### `packages/ocr/`
- PaddleOCR integration
- EasyOCR fallback
- Image preprocessing

#### `packages/ai/`
- Ollama LLM integration
- Prompt engineering
- Field normalization

#### `packages/validation/`
- IMEI validation
- Phone number validation
- Currency validation
- Duplicate detection

#### `packages/excel/`
- Workbook creation
- Formatting
- Incremental updates

## 🛠️ Development

### Setup Development Environment

```bash
# Install dev dependencies
make install-dev

# Enable pre-commit hooks
pre-commit install

# Run tests
make test

# Generate coverage report
make coverage

# Format code
make format

# Lint code
make lint
```

### Creating a New Feature

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes, add tests
# ...

# Format and lint
make format
make lint

# Run tests
make test

# Commit with conventional commits
git commit -m "feat: add your feature description"

# Push and create pull request
git push origin feature/your-feature-name
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_validators.py -v

# Run with coverage
pytest tests/ --cov=packages --cov=apps --cov-report=html

# Run specific marker
pytest -m unit
pytest -m integration
pytest -m e2e
```

### Database Migrations

```bash
# Create new migration
alembic -c packages/database/alembic.ini revision --autogenerate -m "Add users table"

# Apply migrations
alembic -c packages/database/alembic.ini upgrade head

# Rollback one migration
alembic -c packages/database/alembic.ini downgrade -1
```

## 🐳 Docker

### Build and Run

```bash
# Build image
docker build -t fdia:latest .

# Run with compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Services

- **PostgreSQL** - Port 5432
- **Redis** - Port 6379
- **API** - Port 8000
- **Desktop** - Port 8501

## 📚 API Documentation

Start the API server and visit:
- **Swagger UI** - http://localhost:8000/docs
- **ReDoc** - http://localhost:8000/redoc

## 📖 Documentation

- [Architecture Guide](docs/architecture/README.md)
- [API Reference](docs/api/README.md)
- [Deployment Guide](docs/deployment/README.md)
- [User Guide](docs/user-guide/README.md)

## 🔐 Security

- Environment-based configuration
- Encrypted credentials
- SQL injection prevention (SQLAlchemy parameterization)
- CORS configuration
- JWT authentication ready
- HTTPS support

See [SECURITY.md](SECURITY.md) for detailed security guidelines.

## 📊 Milestones

- ✅ Repository bootstrap
- ✅ Python workspace setup
- ✅ Configuration system
- ✅ Logging framework
- ⏳ Database schema
- ⏳ Alembic migrations
- ⏳ Worker framework
- ...

See [docs/milestones/](docs/milestones/) for detailed roadmap.

## 🤝 Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style
- Commit conventions
- Pull request process
- Testing requirements

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Deep Tripathi** - Initial architecture and setup

## 🙏 Acknowledgments

- FastAPI community
- SQLAlchemy team
- PaddleOCR developers
- Flet framework maintainers

---

**Last Updated:** 2026-06-29  
**Version:** 0.1.0
