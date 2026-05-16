.PHONY: help install dev up down shell migrate migrations test lint format typecheck clean

PYTHON = uv run python
DJANGO = $(PYTHON) manage.py
SETTINGS_DEV = DJANGO_SETTINGS_MODULE=config.settings.development

help:
	@echo "Blog Platform — available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies with uv
	uv sync

dev: ## Start development server
	$(SETTINGS_DEV) $(DJANGO) runserver

up: ## Start all services with Docker Compose
	docker compose up -d

down: ## Stop all Docker services
	docker compose down

shell: ## Open Django shell
	$(SETTINGS_DEV) $(DJANGO) shell_plus

migrate: ## Apply migrations
	$(SETTINGS_DEV) $(DJANGO) migrate

migrations: ## Create new migrations
	$(SETTINGS_DEV) $(DJANGO) makemigrations

superuser: ## Create a superuser
	$(SETTINGS_DEV) $(DJANGO) createsuperuser

collectstatic: ## Collect static files
	$(SETTINGS_DEV) $(DJANGO) collectstatic --noinput

test: ## Run test suite
	uv run pytest

test-cov: ## Run tests with coverage report
	uv run pytest --cov --cov-report=html

lint: ## Lint with ruff
	uv run ruff check .

lint-fix: ## Fix linting issues automatically
	uv run ruff check --fix .

format: ## Format with black
	uv run black .

typecheck: ## Type check with pyright
	uv run pyright

pre-commit: ## Run pre-commit hooks on all files
	uv run pre-commit run --all-files

clean: ## Remove python cache files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; \
	find . -name "*.pyc" -delete; \
	find . -name ".coverage" -delete; \
	rm -rf htmlcov/

logs: ## Tail docker compose logs
	docker compose logs -f

rebuild: ## Rebuild and restart docker services
	docker compose up -d --build

celery: ## Start celery worker (dev)
	$(SETTINGS_DEV) uv run celery -A config worker -l info

celery-beat: ## Start celery beat (dev)
	$(SETTINGS_DEV) uv run celery -A config beat -l info
