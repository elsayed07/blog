from __future__ import annotations

import structlog
from celery import shared_task

logger = structlog.get_logger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def publish_scheduled_posts_task(self: object) -> int:
    from .services import publish_scheduled_posts
    try:
        count = publish_scheduled_posts()
        logger.info("task.publish_scheduled_posts.complete", count=count)
        return count
    except Exception as exc:
        logger.error("task.publish_scheduled_posts.failed", error=str(exc))
        raise self.retry(exc=exc)


@shared_task
def rebuild_search_vectors_task() -> None:
    from django.contrib.postgres.search import SearchVector
    from .models import Post
    vector = (
        SearchVector("title", weight="A", config="english")
        + SearchVector("excerpt", weight="B", config="english")
        + SearchVector("body", weight="C", config="english")
    )
    updated = Post.all_objects.filter(deleted_at__isnull=True).update(search_vector=vector)
    logger.info("task.rebuild_search_vectors.complete", updated=updated)
