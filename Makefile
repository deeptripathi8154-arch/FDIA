.PHONY: help install install-dev clean lint format test coverage run-api run-worker run-desktop migrate seed docker-up docker-down docs

help:
	@echo "FDIA Development Commands"
	@echo "========================="
	@echo "make install          - Install dependencies"
	@echo "make install-dev      - Install dev dependencies"
	@echo "make clean            - Remove build artifacts and cache"
	@echo "make lint             - Run linters (ruff, mypy)"
	@echo "make format           - Format code (black, isort)"
	@echo "make test             - Run all tests"
	@echo "make coverage         - Generate coverage report"
	@echo "make run-api          - Start FastAPI server"
	@echo "make run-worker       - Start worker process"
	@echo "make run-desktop      - Start desktop app"
	@echo "make migrate          - Run database migrations"
	@echo "make seed             - Seed database with sample data"
	@echo "make docker-up        - Start Docker services"
	@echo "make docker-down      - Stop Docker services"
	@echo "make docs             - Generate API documentation"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache htmlcov .coverage build dist *.egg-info

lint:
	ruff check .
	mypy packages apps tests

format:
	black .
	isort .

test:
	pytest tests/ -v --cov=packages --cov=apps

coverage:
	pytest tests/ --cov=packages --cov=apps --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

run-api:
	uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000

run-worker:
	python -m apps.worker.main

run-desktop:
	python -m apps.desktop.main

migrate:
	alembic -c packages/database/alembic.ini upgrade head

seed:
	python scripts/seed_database.py

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docs:
	@echo "Generating API documentation..."
	@echo "Visit http://localhost:8000/docs after starting the API"
