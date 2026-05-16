from __future__ import annotations

from django.db.models import Count, Q, QuerySet

from apps.authors.models import AuthorProfile


def get_author_profile(username: str) -> AuthorProfile:
    return (
        AuthorProfile.objects.select_related("user")
        .annotate(post_count=Count("user__posts", filter=Q(user__posts__status="published")))
        .get(user__username=username)
    )


def get_all_authors() -> QuerySet[AuthorProfile]:
    return (
        AuthorProfile.objects.select_related("user")
        .annotate(post_count=Count("user__posts"))
        .filter(post_count__gt=0)
        .order_by("-post_count")
    )
