# Blog Platform

A production-grade Django 5 blog platform — professionally rebuilt from the Django-5-By-Example tutorial with modern engineering standards.

## Architecture Overview

```
blog/
├── config/               # Django configuration (split settings)
│   └── settings/
│       ├── base.py       # Shared settings
│       ├── development.py
│       ├── production.py
│       └── test.py
├── apps/
│   ├── posts/            # Core post domain (models, services, selectors, views, API, tasks)
│   ├── comments/         # Comment domain with moderation workflow
│   └── authors/          # Author profiles
├── core/
│   └── users/            # Custom User model (UUID pk, email-based auth)
├── shared/               # Cross-cutting: base models, pagination, utils
├── infrastructure/       # Nginx config, deployment
├── templates/            # Tailwind CSS + HTMX templates
└── tests/                # pytest suite with factory_boy
```

## What Makes This Production-Grade

| Concern | Tutorial Approach | This Implementation |
|---------|------------------|---------------------|
| User model | Django default `User` | Custom `User` with UUID pk, email login |
| Architecture | Fat views | Services / Selectors / Views (clean separation) |
| Post body | Raw `TextField` | Markdown → HTML render + bleach sanitization |
| Slug | `unique_for_date` | Globally unique with collision resolution |
| Publishing | Simple status field | Draft → Scheduled → Published workflow with Celery |
| Search | Trigram similarity | PostgreSQL full-text search + trigram combined |
| Comments | Anonymous name strings | Authenticated + guest with moderation pipeline |
| Soft deletes | Hard deletes | `deleted_at` soft-delete on Posts and Comments |
| Caching | None | Redis cache, Celery for async, scheduled jobs |
| API | None | Django Ninja (typed, OpenAPI auto-docs at `/api/v1/docs`) |
| Tests | Empty `tests.py` | pytest + factory_boy, business logic coverage |
| Settings | Single `settings.py` | Split: base / development / production / test |
| Docker | Minimal | Multi-stage build, health checks, nginx, celery beat |
| CI | None | GitHub Actions: lint, type-check, tests, coverage |

## Quick Start

```bash
# Install dependencies
uv sync

# Copy and configure environment
cp .env.example .env
# Edit .env with your values

# Start services
docker compose up -d

# Run migrations
make migrate

# Create superuser
make superuser

# Start dev server
make dev
```

## Using Docker (recommended)

```bash
make up       # Start all services
make down     # Stop all services
make logs     # Tail logs
make shell    # Django shell_plus
```

## Tech Stack

- **Python 3.13** + **Django 5.2**
- **PostgreSQL 17** — primary database, full-text search
- **Redis 7** — caching + Celery broker
- **Celery** — async tasks (scheduled publishing, search vector rebuild)
- **Django Ninja** — typed REST API with OpenAPI docs
- **HTMX** — progressive enhancement (live search, reactions, comments)
- **TailwindCSS** — responsive, dark-mode-capable UI
- **WhiteNoise** — static file serving
- **structlog** — structured JSON logging
- **uv** — fast dependency management
- **Ruff + Black + Pyright** — linting, formatting, type checking
- **pytest + factory_boy** — testing
- **pre-commit** — automated code quality gates
- **GitHub Actions** — CI/CD pipeline

## API

OpenAPI documentation available at `/api/v1/docs` when running.

Key endpoints:
- `GET /api/v1/posts/` — paginated post list (filter by `?tag=`)
- `GET /api/v1/posts/{slug}/` — post detail
- `GET /api/v1/posts/search/?q=` — full-text search

## Architecture Decisions

### Services / Selectors Pattern
Business logic lives in `services.py` (write operations) and `selectors.py` (read queries). Views are thin — they parse request data, call a service/selector, and return a response. This makes logic independently testable without HTTP overhead.

### Custom User Model
Starting with a custom User model eliminates the painful migration required when you need to extend Django's default mid-project. Email is the login identifier; UUID primary key avoids enumeration.

### Soft Deletes
Posts and comments use `deleted_at` instead of hard deletion. This enables undelete, audit trails, and prevents broken foreign key references in analytics.

### Markdown + Bleach
Post bodies are authored in Markdown (stored as raw text, rendered to `body_html` on save). Bleach sanitizes the output against an allowlist, preventing XSS.

### Scheduled Publishing
A Celery beat task runs every 60 seconds to publish posts whose `published_at` has passed and status is `scheduled`. No cron jobs, no management commands to remember.

### PostgreSQL Full-Text Search
`SearchVector` + `SearchQuery` with trigram fallback gives quality relevance ranking without Elasticsearch complexity. The search vector is rebuilt hourly via a Celery task.

## Deployment

```bash
# Production deployment
docker compose -f docker-compose.prod.yml up -d

# Set these env vars in production:
# SECRET_KEY, DATABASE_URL, REDIS_URL, SENTRY_DSN
# AWS_STORAGE_BUCKET_NAME (for media storage)
```

## Scaling Notes

- **Horizontal scaling**: stateless web workers behind nginx load balancer
- **Database**: add read replicas, use `DATABASE_REPLICA_URL` for read traffic
- **Cache**: Redis cluster for high availability
- **Media**: S3 + CloudFront CDN (configured via `AWS_*` env vars)
- **Search**: upgrade to Elasticsearch/OpenSearch if trigram performance degrades at scale
- **Celery**: dedicated worker pools per task queue as throughput grows
