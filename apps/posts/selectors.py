from __future__ import annotations

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Count, F, Q, QuerySet
from django.utils import timezone
from taggit.models import Tag

from .models import Bookmark, Post, PostStatus


def get_published_posts() -> QuerySet[Post]:
    return Post.objects.all()


def get_post_by_slug(slug: str) -> Post:
    return (
        Post.objects.select_related("author", "author__author_profile")
        .prefetch_related("tags", "comments")
        .get(slug=slug)
    )


def get_posts_by_tag(tag_slug: str) -> QuerySet[Post]:
    tag = Tag.objects.get(slug=tag_slug)
    return Post.objects.filter(tags__in=[tag])


def get_posts_by_author(username: str) -> QuerySet[Post]:
    return Post.objects.filter(author__username=username)


def get_featured_posts(limit: int = 5) -> QuerySet[Post]:
    return Post.objects.filter(is_featured=True)[:limit]


def get_related_posts(post: Post, limit: int = 4) -> QuerySet[Post]:
    tag_ids = post.tags.values_list("id", flat=True)
    return (
        Post.objects.filter(tags__in=tag_ids)
        .exclude(pk=post.pk)
        .annotate(shared_tags=Count("tags"))
        .order_by("-shared_tags", "-published_at")[:limit]
    )


def get_trending_posts(days: int = 7, limit: int = 5) -> QuerySet[Post]:
    since = timezone.now() - timezone.timedelta(days=days)
    return (
        Post.objects.filter(published_at__gte=since)
        .order_by("-view_count")[:limit]
    )


def search_posts(query: str) -> QuerySet[Post]:
    if not query:
        return Post.objects.none()

    search_query = SearchQuery(query, search_type="websearch")
    vector = SearchVector("title", weight="A") + SearchVector("excerpt", weight="B") + SearchVector("body", weight="C")

    return (
        Post.objects.annotate(
            rank=SearchRank(vector, search_query),
            similarity=TrigramSimilarity("title", query),
        )
        .filter(Q(rank__gte=0.05) | Q(similarity__gte=0.1))
        .order_by("-rank", "-similarity")
    )


def get_user_bookmarks(user_id: object) -> QuerySet[Bookmark]:
    return (
        Bookmark.objects.filter(user_id=user_id)
        .select_related("post", "post__author")
        .order_by("-created_at")
    )


def get_scheduled_posts_due() -> QuerySet[Post]:
    return Post.all_objects.filter(
        status=PostStatus.SCHEDULED,
        published_at__lte=timezone.now(),
        deleted_at__isnull=True,
    )
