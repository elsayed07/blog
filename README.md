<div align="center">

# Blog Platform

**A production-grade Django 5 blog platform — built with modern engineering standards.**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![CI](https://img.shields.io/github/actions/workflow/status/elsayed07/blog/ci.yml?style=flat-square&label=CI&logo=github)](https://github.com/elsayed07/blog/actions)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[Features](#features) · [Tech Stack](#tech-stack) · [Quick Start](#quick-start) · [API](#api) · [Architecture](#architecture) · [Deployment](#deployment)

</div>

---

## Screenshots

> _Screenshots coming soon — run locally with `make up` to see it in action._

---

## Features

### Content
- **Rich post editor** — write in Markdown, rendered to sanitized HTML (XSS-safe via Bleach)
- **Publishing workflow** — Draft → Scheduled → Published → Archived, with Celery-powered auto-publishing
- **Tagging system** — case-insensitive tags with dedicated tag browsing pages
- **Featured & trending posts** — curated featured section + trending sidebar by view count
- **Reading time estimation** — auto-calculated on every save
- **Cover images & OG metadata** — per-post cover images, custom Open Graph title/description/image

### Discovery
- **Full-text search** — PostgreSQL `SearchVector` + GIN index, with trigram fallback for fuzzy matching
- **RSS & Atom feeds** — at `/feed/rss/` and `/feed/atom/`
- **XML sitemap** — auto-generated at `/sitemap.xml` for SEO

### Engagement
- **Post reactions** — Like, Love, Insightful; togglable, login-gated
- **Bookmarks** — per-user saved post list
- **Comments** — threaded replies, guest commenting (name + email), full moderation pipeline (pending → approved/rejected/spam)
- **Live search** — HTMX-powered search results without a page reload

### Platform
- **REST API** — Django Ninja with OpenAPI/Swagger docs at `/api/v1/docs`
- **Author profiles** — dedicated author pages with post listings
- **Post analytics** — view count, unique views, and share tracking
- **Soft deletes** — posts and comments use `deleted_at`; nothing is lost permanently
- **Admin panel** — full Django Admin with rich filtering and search

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.13, Django 5.2 |
| **Database** | PostgreSQL 17 (full-text search, GIN indexes) |
| **Cache / Broker** | Redis 7 |
| **Task Queue** | Celery + Celery Beat |
| **API** | Django Ninja (OpenAPI auto-docs) |
| **Frontend** | HTMX + Tailwind CSS |
| **Static Files** | WhiteNoise |
| **Image Processing** | Pillow + django-imagekit |
| **Logging** | structlog (structured JSON) |
| **Error Tracking** | Sentry SDK |
| **File Storage** | Local / AWS S3 + django-storages |
| **Package Manager** | uv |
| **Linting / Formatting** | Ruff + Black |
| **Type Checking** | Pyright |
| **Testing** | pytest + factory\_boy + pytest-cov |
| **CI/CD** | GitHub Actions + Codecov |
| **Containerization** | Docker (multi-stage) + Docker Compose |
| **Production Server** | Gunicorn + Nginx |

---

## Quick Start

### Using Docker (recommended)

```bash
# 1. Clone the repo
git clone https://github.com/elsayed07/blog.git
cd blog

# 2. Copy environment file and configure
cp .env.example .env

# 3. Start all services (web, db, redis, celery, celery-beat)
make up

# 4. Run migrations
docker compose exec web uv run python manage.py migrate

# 5. Seed sample posts
docker compose exec web uv run python manage.py seed_posts

# 6. Create a superuser
docker compose exec -e DJANGO_SUPERUSER_PASSWORD=yourpassword web \
  uv run python manage.py createsuperuser \
  --email admin@blog.local --username admin --noinput
```

Visit **http://localhost:8000** — admin panel at **http://localhost:8000/admin/**

### Local Development (without Docker)

```bash
# Install uv
pip install uv

# Install dependencies
uv sync

# Copy and configure environment
cp .env.example .env

# Apply migrations
make migrate

# Start dev server
make dev
```

> Requires PostgreSQL and Redis running locally. Set `DATABASE_URL` and `REDIS_URL` in `.env`.

---

## Available Commands

```bash
make up           # Start all Docker services
make down         # Stop all Docker services
make logs         # Tail Docker logs
make shell        # Open Django shell_plus
make migrate      # Apply migrations
make migrations   # Create new migrations
make superuser    # Create superuser (interactive)
make test         # Run test suite
make test-cov     # Run tests with HTML coverage report
make lint         # Lint with Ruff
make lint-fix     # Auto-fix lint issues
make format       # Format with Black
make typecheck    # Type check with Pyright
make rebuild      # Rebuild and restart Docker services
```

---

## Environment Variables

Copy `.env.example` and set the following:

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Django secret key | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `REDIS_URL` | Redis connection string | Yes |
| `DEBUG` | Enable debug mode (`True`/`False`) | No |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | Production |
| `SENTRY_DSN` | Sentry error tracking DSN | No |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket for media files | No |
| `EMAIL_HOST` | SMTP host for emails | No |

---

## API

Auto-generated OpenAPI docs: **http://localhost:8000/api/v1/docs**

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/posts/` | Paginated post list (filter: `?tag=`) |
| `GET` | `/api/v1/posts/{slug}/` | Post detail |
| `GET` | `/api/v1/posts/search/?q=` | Full-text search |

---

## Architecture

```
blog/
├── config/                 # Django configuration
│   └── settings/
│       ├── base.py         # Shared settings
│       ├── development.py  # Dev overrides
│       ├── production.py   # Prod hardening
│       └── test.py         # Test isolation
├── apps/
│   ├── posts/              # Core domain
│   │   ├── models.py       # Post, Reaction, Bookmark, Analytics
│   │   ├── services.py     # Write operations (business logic)
│   │   ├── selectors.py    # Read queries
│   │   ├── views.py        # Thin HTTP layer
│   │   ├── tasks.py        # Celery tasks
│   │   └── api/            # Django Ninja REST API
│   ├── comments/           # Threaded comments + moderation
│   └── authors/            # Author profiles
├── core/
│   └── users/              # Custom User model (UUID pk, email auth)
├── shared/                 # Base models, pagination, utilities
├── infrastructure/         # Nginx config
└── tests/                  # pytest suite
```

### Key Design Decisions

**Services / Selectors pattern** — business logic lives in `services.py` (writes) and `selectors.py` (reads). Views are thin; logic is independently testable without HTTP overhead.

**Custom User model from day one** — email-based login, UUID primary key (prevents enumeration), no painful mid-project migrations.

**Soft deletes** — Posts and Comments use `deleted_at` instead of hard deletion. Supports undelete, audit trails, and referential integrity in analytics.

**PostgreSQL full-text search** — `SearchVector` stored in a `GinIndex`-backed field, rebuilt hourly by Celery. Trigram fallback ensures fuzzy matching without Elasticsearch complexity.

**Scheduled publishing** — Celery Beat checks every 60 seconds for posts where `status=scheduled` and `published_at <= now()`. No cron jobs to configure.

---

## Deployment

### Production with Docker

```bash
# Deploy production stack (includes Nginx)
docker compose -f docker-compose.prod.yml up -d

# Collect static files
docker compose exec web uv run python manage.py collectstatic --noinput

# Run migrations
docker compose exec web uv run python manage.py migrate
```

### Required Production Environment Variables

```env
SECRET_KEY=<strong-random-key>
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://host:6379/0
ALLOWED_HOSTS=yourdomain.com
SENTRY_DSN=https://...@sentry.io/...
AWS_STORAGE_BUCKET_NAME=your-bucket   # for media files
```

### Scaling

- **Web workers** — stateless, scale horizontally behind the Nginx load balancer
- **Media storage** — configure `AWS_*` env vars to use S3 + CloudFront
- **Database** — add read replicas for high read traffic
- **Celery** — split into separate worker pools per queue as throughput grows

---

## Testing

```bash
# Run full suite
make test

# With coverage report (outputs to htmlcov/)
make test-cov

# Run a specific test file
uv run pytest tests/test_posts.py -v
```

The test suite uses `factory_boy` for fixtures and `pytest-django` for database handling. Each test run reuses the database schema (`--reuse-db`) for speed.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Install pre-commit hooks: `uv run pre-commit install`
4. Make your changes — pre-commit will enforce linting, formatting, and type checks
5. Run the test suite: `make test`
6. Open a pull request

---

## License

This project is licensed under the [MIT License](LICENSE).
