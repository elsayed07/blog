from __future__ import annotations

import structlog
from django.contrib.postgres.search import SearchVector
from django.db import transaction
from django.utils import timezone

from .models import Bookmark, Post, PostAnalytics, PostReaction, PostStatus

logger = structlog.get_logger(__name__)


def publish_post(post: Post) -> Post:
    if post.status not in (PostStatus.DRAFT, PostStatus.SCHEDULED):
        raise ValueError(f"Cannot publish post in status: {post.status}")
    post.status = PostStatus.PUBLISHED
    post.published_at = post.published_at or timezone.now()
    post.save(update_fields=["status", "published_at", "updated_at"])
    _rebuild_search_vector(post)
    logger.info("post.published", post_id=str(post.id), slug=post.slug)
    return post


def schedule_post(post: Post, publish_at: object) -> Post:
    post.status = PostStatus.SCHEDULED
    post.published_at = publish_at
    post.save(update_fields=["status", "published_at", "updated_at"])
    return post


def archive_post(post: Post) -> Post:
    post.status = PostStatus.ARCHIVED
    post.save(update_fields=["status", "updated_at"])
    return post


@transaction.atomic
def toggle_reaction(post: Post, user: object, reaction: str) -> bool:
    """Returns True if reaction was added, False if removed."""
    existing = PostReaction.objects.filter(post=post, user=user, reaction=reaction).first()
    if existing:
        existing.delete()
        return False
    PostReaction.objects.create(post=post, user=user, reaction=reaction)
    return True


@transaction.atomic
def toggle_bookmark(post: Post, user: object) -> bool:
    """Returns True if bookmarked, False if removed."""
    existing = Bookmark.objects.filter(post=post, user=user).first()
    if existing:
        existing.delete()
        return False
    Bookmark.objects.create(post=post, user=user)
    return True


def record_view(post: Post, user_ip: str) -> None:
    from django.db.models import F
    Post.all_objects.filter(pk=post.pk).update(view_count=F("view_count") + 1)
    analytics, _ = PostAnalytics.objects.get_or_create(post=post)
    PostAnalytics.objects.filter(pk=analytics.pk).update(unique_views=F("unique_views") + 1)


def _rebuild_search_vector(post: Post) -> None:
    vector = (
        SearchVector("title", weight="A", config="english")
        + SearchVector("excerpt", weight="B", config="english")
        + SearchVector("body", weight="C", config="english")
    )
    Post.all_objects.filter(pk=post.pk).update(search_vector=vector)


def publish_scheduled_posts() -> int:
    from .selectors import get_scheduled_posts_due
    posts = get_scheduled_posts_due()
    count = 0
    for post in posts:
        publish_post(post)
        count += 1
    logger.info("scheduled_posts.published", count=count)
    return count
