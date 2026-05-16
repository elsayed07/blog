from __future__ import annotations

from django import template
from django.utils.safestring import mark_safe

from apps.posts.selectors import get_trending_posts

register = template.Library()


@register.inclusion_tag("posts/partials/trending_sidebar.html")
def trending_posts(count: int = 5) -> dict:
    return {"posts": get_trending_posts(limit=count)}


@register.filter
def reading_time_label(minutes: int) -> str:
    return f"{minutes} min read"


@register.filter
def reaction_icon(reaction: str) -> str:
    icons = {"like": "👍", "love": "❤️", "insightful": "💡"}
    return icons.get(reaction, "👍")
